from randblog.rss import entry_collection
from randblog.corpus.item import Item
from randblog.crawler import clean_link

from bs4 import BeautifulSoup

class Entry(object):

    def __init__(self, feed, id, data = None):
        self._feed = feed
        self._id = id
        self._info = entry_collection.find_one({'id':self._id})
        self.__cleaned_soup = None
        self.__cleaned_links = None
        if self._info:
            self._info.update(data)
            self._info['feed'] = feed.info['_id']
            self._info['feed_name'] = feed.name
        else:
            self._info = data
            self._info['feed'] = feed.info['_id']
            self._info['feed_name'] = feed.name

    @property
    def id(self):
        return self._id

    @property
    def feed(self):
        return self._feed

    @property
    def info(self):
        return self._info

    @property
    def link(self):
        return self._info['link']

    def save(self):
        entry_collection.save(self._info)

    def _content_soup(self):
        if 'content' in self._info:
            return BeautifulSoup(self._info['content'][0]['value'], 'html5lib')
        else:
            return BeautifulSoup(self._info['summary'], 'html5lib')

    @property
    def cleaned_soup(self):
        if self.__cleaned_soup is None:
            soup = self._content_soup()
            if 'clean_actions' in self.feed.info:
                for action in self.feed.info['clean_actions']:
                    for tag in soup.select(action['selector']):
                        if 'match_text' in action and tag.get_text() != action['match_text']:
                            continue
                        if 'contains_text' in action and tag.get_text().find(action['contains_text']) == -1:
                            continue
                        if action['task'] == 'remove':
                            tag.decompose()
            self.__cleaned_soup = soup
        return self.__cleaned_soup

    @property
    def cleaned_links(self):
        if self.__cleaned_links is None:
            self.__cleaned_links = [{'href':self._info['link'], 'title': self._info['title']}]
            soup = self._content_soup()
            for l in soup.select('a[href]'):
                href = clean_link(l['href'])
                if not href is None:
                    self.__cleaned_links.append({'title': l.get_text().strip(), 'href': href})
        return self.__cleaned_links

    def _stats_key(self):
        return {
            'source': {
                'type': 'rss',
                'rss_feed_name':    self._info['feed_name'],
                'rss_feed_id':      self._info['feed'],
                'rss_feed_entry':   self.id,
                'rss_feed_entry_id':self._info['_id']
            }
        }

    def clean(self):
        key = self._stats_key()
        key.update({
            'title': self._info['title'],
            'text': self.cleaned_soup.get_text().strip(),
            'published': self._info['published'],
            'updated': self._info['updated'],
            'links': self.cleaned_links
        })

        if 'corpus_item' in self.info and self.info['corpus_item'] and not self.corpus_item._data is None:
            item = self.corpus_item
            item._data.update(key)
            item.save()
            item.extract_crawl_links()
        else:
            item = Item(key)
            item.save()
            self.info['corpus_item'] = item.id
            self.save()
            item.extract_crawl_links()

    @property
    def corpus_item(self):
        if not hasattr(self, '_corpus_item') or self._corpus_item is None:
            self._corpus_item = Item.find_one({'_id': self.info['corpus_item']})
        return self._corpus_item
