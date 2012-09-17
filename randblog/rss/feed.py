from randblog.rss import feed_collection, entry_collection
from randblog.rss.entry import Entry
import feedparser

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

    @classmethod
    def find(cls, query={}):
        return map(lambda f: cls(f['name'], f['url'], f), feed_collection.find(query))

    def __init__(self, name, url=None, info=None):
        self._name = name
        if not url is None:
            self._url = url
        self._info = info
        self._feed = None
        self._feed_status = None
        self._entries = {} 

    def _db_entries_load(self):
        for e in entry_collection.find({'feed': self.info['_id']}):
            self._entries[e['id']] = Entry(self, e['id'], e)

    def _db_load(self):
        if self._info is None:
            self._info = feed_collection.find_one({'name': self._name})
            if self._info is None:
                self._info = {'name': self._name, 'url': self._url}
                self._info['title'] = self.feed.feed['title']
                self._info['subtitle'] = self.feed.feed['subtitle']
                self._info['link'] = self.feed.feed['link']
                self._info['status'] = self._feed_status
                feed_collection.insert(self._info)
                self._db_entries_load()

    def _get_feed(self, update = False):
        if update and (not self._info is None) and ('status' in self._info):
            opts = {}
            if 'etag' in self._info['status']:
                opts['etag'] = self._info['status']['etag']
            if 'modified' in self._info['status']:
                opts['modified'] = self._info['status']['modified']
            feed = feedparser.parse(self.url, **opts)
            if feed.status == 304:
                feed = None
        else:
            feed = feedparser.parse(self.url)
        return feed
        

    def _feed_load(self, update = False):
        feed = self._get_feed(update)
        if not feed is None:
            print "Feed Data Modified"
            self._feed = feed
            self._feed_status = {
                'version': self._feed.version,
                'encoding': self._feed.encoding,
            }
            if hasattr(self._feed, 'etag'):
                self._feed_status['etag'] = self._feed.etag
            if hasattr(self._feed, 'updated_parsed'):
                self._feed_status['updated'] = tuple(self._feed.updated_parsed)
            if hasattr(self._feed, 'modified_parsed'):
                self._feed_status['modified'] = tuple(self._feed.modified_parsed)
            if not self._info is None:
                self._info['status'] = self._feed_status
                feed_collection.save(self._info)

                for e_data in feed.entries:
                    data = {}
                    for key, value in e_data.items():
                        if key in ('updated', 'modified', 'published'):
                            pass
                        elif key == 'updated_parsed':
                            data['updated'] = tuple(value)
                        elif key == 'modified_parsed':
                            data['modified'] = tuple(value)
                        elif key == 'published_parsed':
                            data['published'] = tuple(value)
                        else:
                            data[key] = value
                    e = Entry(self, data['id'], data)
                    self._entries[e.id] = e
                    e.clean()
                    e.save()

    def update(self, update = True):
        self._feed_load(update)

    def clean(self):
        def t(e):
            e.clean()
            e.save()
        self._each_entry(t)

    def stats_collect(self):
        def t(e):
            e.stats_collect()
            e.save()
        self._each_entry(t)

    def _each_entry(self, task):
        self._db_entries_load()
        for e in self.entries.values():
            task(e)

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

    @property
    def entries(self):
        if not hasattr(self, '_entries') or self._entries is None:
            self._db_load_entries()
        return self._entries        

    def __repr__(self):
        return '<Feed %s ("%s": %s)>' % (self.name, self.title, self.url)
