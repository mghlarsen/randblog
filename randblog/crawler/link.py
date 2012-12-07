from randblog.crawler import link_collection

class Link(object):
    def __init__(self, url=None, info={}):
        if not url is None:
            self._info = info
            self._info['url'] = url
        else:
            self._info = info

    @property
    def saved(self):
        return '_id' in self._info

    @property
    def url(self):
        return self._info['url']

    def save(self):
        link_collection.save(self._info)

    @classmethod
    def find(cls, url):
        res = link_collection.find_one({'url':url})
        if res is None:
            return cls(url)
        else:
            return cls(info=res)

