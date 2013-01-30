from randblog.crawler import link_collection

class Link(object):
    def __init__(self, url=None, info=None):
        if info is None:
            info = {'sources':[]}
        if not url is None:
            self._info = info
            self._info['url'] = url
            self._info['sources'] = []
        else:
            self._info = info

    @property
    def saved(self):
        return '_id' in self._info

    @property
    def url(self):
        return self._info['url']

    @property
    def id(self):
        if not '_id' in self._info:
            return None
        return self._info['_id']

    def save(self):
        link_collection.save(self._info)

    def ensure_source(self, id):
        if not 'sources' in self._info:
            self._info['sources'] = []
        if not id in self._info['sources']:
            self._info['sources'].append(id)
            return False
        else:
            return True

    @classmethod
    def find(cls, **kw):
        res = link_collection.find_one(kw)
        if (res is None) and ('url' in kw) and not ('_id' in kw):
            return cls(kw['url'])
        elif res is None:
            return None
        else:
            return cls(info=res)

