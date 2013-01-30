from randblog.corpus import item_collection
from randblog.corpus.stats import Stats
from randblog.crawler.link import Link

__all__ = ['Item']

class Item(object):
    def __init__(self, data):
        self._data = data

    @classmethod
    def find(cls, query={}):
        return map(lambda i: cls(i), item_collection.find(query))

    @classmethod
    def find_one(cls, query={}):
        return cls(item_collection.find_one(query))

    @property
    def id(self):
        return self._data['_id']

    def save(self):
        item_collection.save(self._data)

    def stats_collect(self, update = False):
        query = dict(self._data)
        del query['_id']
        del query['text']
        stats = Stats('item', query)
        if len(stats.get_ids()) == 0 or update:
            stats.clear()
            stats.collect_words(self.get_split_words())
            stats.save()
            self._data['stats'] = stats.get_ids()

    def get_split_words(self):
        words = self._data['text'].split()
        while len(words) > 0 and words[-1] == '|':
            words.pop()
        return words

    def extract_crawl_links(self):
        updated = 0
        link_updated = 0
        existing = 0
        need_save = False
        for link in self._data['links']:
            if 'id' in link:
                l = Link.find(_id = link['id'], url = link['href'])
                if (l is None) or (not l.saved) or (l.url != link['href']):
                    del link['id']
                    need_save = True
                else:
                    existing += 1
                    if not l.ensure_source(self.id):
                        l.save()
                    continue

            l = Link.find(url=link['href'])
            if not l.saved:
                updated += 1
            else:
                link_updated += 1
            l.ensure_source(self.id)
            l.save()
            link['id'] = l.id
            need_save = True
        if need_save:
            self.save()
        return len(self._data['links']), existing, link_updated, updated

