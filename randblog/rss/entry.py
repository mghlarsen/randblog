from randblog.rss import entry_collection

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

