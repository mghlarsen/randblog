from mongoengine import *

__all__ = ['CorpusItem', 'CorpusItemLink', 'CorpusItemSource', 'CORPUS_ITEM_SOURCE_TYPES']

CORPUS_ITEM_SOURCE_TYPES = ('rss', 'link')

class CorpusItemSource(EmbeddedDocument):
    type = StringField(required=True, choices = CORPUS_ITEM_SOURCE_TYPES)
    entry = ReferenceField('Entry', dbref=False)
    link = ReferenceField('Link', dbref=False)

class CorpusItemLink(EmbeddedDocument):
    href = StringField(required=True)
    title = StringField(required=True)
    id = ReferenceField('Link', dbref=False)

class CorpusItem(DynamicDocument):
    title = StringField(required=True)
    text = StringField()
    published = DateTimeField()
    updated = DateTimeField()
    source = EmbeddedDocumentField(CorpusItemSource, required=True)
    links = ListField(EmbeddedDocumentField(CorpusItemLink))

    def get_split_words(self):
        words = self.text.split()
        while len(words) > 0 and words[-1] == '|':
            words.pop()
        return words

    def extract_crawl_links(self):
        from randblog.crawler.link import Link
        updated = 0
        link_updated = 0
        existing = 0
        need_save = False
        for link in self.links:
            if link.id is None:
                need_save = True
                url = clean_link(link.href)
                link.id, created = Link.get_or_create(url = url)
            if not self in link.id.sources:
                need_save = True
                link.id.sources.append(self)
        if need_save:
            self.save()
