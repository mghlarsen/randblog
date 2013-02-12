from randblog.rss import convert_time_tuple
from randblog.rss.feed import Feed
from datetime import datetime
from mongoengine import *
from bs4 import BeautifulSoup

__all__ = ['Entry', 'EntryLink', 'EntryAuthorDetail', 'EntryTag', 'EntryContentDetail']

class EntryContentDetail(EmbeddedDocument):
    base = StringField()
    type = StringField()
    language = StringField()
    value = StringField()

class EntryTag(EmbeddedDocument):
    term = StringField(required=True)
    scheme = StringField()
    label = StringField()

class EntryAuthorDetail(EmbeddedDocument):
    name = StringField(required=True)

class EntryLink(EmbeddedDocument):
    href = StringField(required=True)
    type = StringField(required=True)
    rel = StringField(required=True)

class Entry(DynamicDocument):
    feed = ReferenceField('Feed', dbref=False, required=True)
    entry_id = StringField(required=True) #This is the ID in the RSS feed
    title = StringField(required=True)
    title_detail = EmbeddedDocumentField(EntryContentDetail)
    subtitle = StringField()
    subtitle_detail = EmbeddedDocumentField(EntryContentDetail)
    corpus_item = ReferenceField('CorpusItem', dbref=False)
    links = ListField(ReferenceField('Link', dbref=False))
    author = StringField()
    published = DateTimeField()
    updated = DateTimeField()
    summary = StringField()
    summary_detail = EmbeddedDocumentField(EntryContentDetail)
    content = ListField(EmbeddedDocumentField(EntryContentDetail))
    tags = ListField(EmbeddedDocumentField(EntryTag))
    author_detail = EmbeddedDocumentField(EntryAuthorDetail)
    links = ListField(EmbeddedDocumentField(EntryLink))
    media_info = DictField()
    extra_info = DictField()

    def set_datetime_field(self, fieldName, attr, value):
        suffix = attr[len(fieldName)+1:]
        if suffix == '' and isinstance(value, datetime):
            setattr(self, fieldName, value)
        elif suffix == 'parsed':
            setattr(self, fieldName, convert_time_tuple(value))

    def populate_from_dict_info(self, info):
        for attr, value in info.items():
            if attr == 'title':
                self.title = value
            elif attr == 'link':
                if 'feedburner_origlink' not in info:
                    self.link = value
            elif attr == 'author':
                self.author = value
            elif attr == 'published' or attr == 'published_parsed':
                self.set_datetime_field('published', attr, value)
            elif attr == 'updated':
                self.set_datetime_field('updated', attr, value)
            elif attr == 'summary':
                self.summary = value
            elif attr == 'title_detail':
                self.title_detail = EntryContentDetail(**value)
            elif attr == 'summary_detail':
                self.summary_detail = EntryContentDetail(**value)
            elif attr == 'content':
                self.content = [EntryContentDetail(**c) for c in value]
            elif attr == 'tags':
                self.tags = [EntryTag(**t) for t in value]
            elif attr == 'feedburner_origlink':
                self.link = value
            elif attr == 'author_detail':
                self.author_detail = EntryAuthorDetail(**value)
            elif attr == 'links':
                for l in value:
                    self.links.append(EntryLink(**l))
            elif attr == 'subtitle':
                self.subtitle = value
            elif attr == 'subtitle_detail':
                self.subtitle_detail = EntryContentDetail(**value)
            elif attr in ['_id', 'id', 'feed_name', 'feed', 'cleaned']:
                pass
            elif attr in ['wfw_commentrss', 'guidislink', 'comments', 'authors', 'href']:
                self.extra_info[attr] = value
            elif attr in ['slash_comments', 'slash_department', 'slash_section', 'slash_hit_parade']:
                self.extra_info[attr] = value
            elif attr in ['itunes_duration', 'itunes_keywords', 'itunes_explicit', 'media_content', 'media_thumbnail', 'go_thumbnail']:
                self.media_info[attr] = value
            else:
                self.extra_info[attr] = value

    def clean(self):
        from randblog.corpus.item import CorpusItem, CorpusItemLink, CorpusItemSource
        try:
            item = CorpusItem.objects.get(source__type = 'rss', source__entry = self)
            created = False
        except CorpusItem.DoesNotExist:
            item = CorpusItem()
            item.source = CorpusItemSource(type = 'rss', entry = self)
            created = True
        item.title = self.title
        item.text = self.cleaned_soup.get_text().strip()
        item.published = self.published
        item.updated = self.updated
        for l in self.cleaned_links:
            item.links.append(CorpusItemLink(**l))
        item.save()

    def _content_soup(self):
        if len(self.content) > 0:
            return BeautifulSoup(self.content[0].value, 'html5lib')
        else:
            return BeautifulSoup(self.summary, 'html5lib')

    @property
    def cleaned_soup(self):
        if not hasattr(self, '__cleaned_soup'):
            soup = self._content_soup()
            for action in self.feed.clean_actions:
                for tag in soup.select(action.selector):
                    if action.match_text and tag.get_text() != action.match_text:
                        continue
                    if action.contains_text and tag.get_text().find(action.contains_text) == -1:
                        continue
                    if action.task == 'remove':
                        tag.decompose()
            self.__cleaned_soup = soup
        return self.__cleaned_soup

    @property
    def cleaned_links(self):
        if not hasattr(self, '__cleaned_links'):
            self.__cleaned_links = [{'href':self.link, 'title':self.title}]
            soup = self._content_soup()
            for l in soup.select('a[href]'):
                self.__cleaned_links.append({'title': l.get_text().strip(), 'href': l['href']})
        return self.__cleaned_links
