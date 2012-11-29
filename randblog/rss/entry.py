from randblog.rss import entry_collection
from randblog.corpus.item import Item

from bs4 import BeautifulSoup

class Entry(object):

    def __init__(self, feed, id, data = None):
        self._feed = feed
        self._id = id
        self._info = entry_collection.find_one({'id':self._id})
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

    def _cleaned_soup(self):
        soup = BeautifulSoup(self._info['summary'], 'html5lib')
        if 'clean_actions' in self.feed.info:
            for action in self.feed.info['clean_actions']:
                for tag in soup.select(action['selector']):
                    if 'match_text' in action and tag.get_text() != action['match_text']:
                        continue
                    if 'contains_text' in action and tag.get_text().find(action['contains_text']) == -1:
                        continue
                    if action['task'] == 'remove':
                        tag.decompose()
        return soup

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
            'text': self._cleaned_soup().get_text().strip()
        })
        if 'corpus_item' in self.info and self.info['corpus_item'] and not self.corpus_item._data is None:
            item = self.corpus_item
            item._data.update(key)
        else:
            item = Item(key)
            item.save()
            self.info['corpus_item'] = item.id
            self.save()

    @property
    def corpus_item(self):
        if not hasattr(self, '_corpus_item') or self._corpus_item is None:
            self._corpus_item = Item.find_one({'_id': self.info['corpus_item']})
        return self._corpus_item
