from randblog.rss import feed_collection
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

    def __init__(self, name, url=None):
        self._name = name
        if not url is None:
            self._url = url
        self._info = None
        self._feed = None
        self._feed_status = None

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

    def _get_feed(self, update = False):
        if update and not self._info is None:
            print "Sending ETag %s and Last Modified %s" % (self._info['status']['etag'], str(self._info['status']['modified']))
            feed = feedparser.parse(self.url, etag = self._info['status']['etag'], modified = self._info['status']['modified'])
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
                'updated': tuple(self._feed.updated_parsed),
                'version': self._feed.version,
                'encoding': self._feed.encoding,
                'etag': self._feed.etag,
                'modified': tuple(self._feed.modified_parsed)
            }
            if not self._info is None:
                self._info['status'] = self._feed_status
                feed_collection.save(self._info)

    def update(self, update = True):
        self._feed_load(update)

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
