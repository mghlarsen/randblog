from randblog.corpus import item_collection
from randblog.corpus.stats import Stats

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

