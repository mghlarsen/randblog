from gevent import monkey; monkey.patch_all()
from pymongo import Connection
import feedparser

db = Connection()['trgtb-DEV']

feed_collection = db['feeds']

class Feed(object):
    @classmethod
    def add(cls, name, url):
        f = cls(name, url)
        f._db_load()
        return f

    @classmethod
    def get(cls, name):
        f = cls(name)
        f._db_load()
        return f

    def __init__(self, name, url=None):
        self._name = name
        if not url is None:
            self._url = url
        self._info = None
        self._feed = None

    def _db_load(self):
        if self._info is None:
            self._info = feed_collection.find_one({'name': self._name})
            if self._info is None:
                self._info = {'name': self._name, 'url': self._url}
                self._info['title'] = self.feed['feed']['title']
                self._info['subtitle'] = self.feed['feed']['subtitle']
                self._info['link'] = self.feed['feed']['link']
                feed_collection.insert(self._info)

    def _feed_load(self):
        self._feed = feedparser.parse(self.url)

    @property
    def feed(self):
        if self._feed is None:
            self._feed_load()
        return self._feed

    @property
    def info(self):
        if self._info is None:
            self._db_load()
        return self._info

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        if self._info is None and hasattr(self, '_url'):
            return self._url
        return self.info['url']

    @property
    def title(self):
        return self.info['title']

    @property
    def subtitle(self):
        return self.info['subtitle']

    @property
    def link(self):
        return self.info['link']

    def __repr__(self):
        return '<Feed %s ("%s": %s)>' % (self.name, self.title, self.url)
