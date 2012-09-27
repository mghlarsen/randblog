from randblog.rss import entry_collection

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

    def clean(self):
        self.info['cleaned'] = {'text': BeautifulSoup(self._info['summary'], 'html5lib').get_text().strip()}
 
    def stats_collect(self):
        content = self.info['cleaned']['text']
        words = content.split() + ['<END>']
        words = map(lambda w: w.replace('.', '<period>').replace('$', '<dollar>'), words)
        stats = {'2gram':{}, '3gram':{}, '4gram':{}, '5gram':{}}

        for i in range(len(words)):
            if i > 0:
                ngram(stats['2gram'], words[i-1:i+1])
            else:
                ngram(stats['2gram'], ('<START>', words[0]))
            if i > 1:
                ngram(stats['3gram'], words[i-2:i+1])
            else:
                ngram(stats['3gram'], (['<START>',] * (2 - i)) + words[:i+1])
            if i > 2:
                ngram(stats['4gram'], words[i-3:i+1])
            else:
                ngram(stats['4gram'], (['<START>',] * (3 - i)) + words[:i+1])
            if i > 3:
                ngram(stats['5gram'], words[i-4:i+1])
            else:
                ngram(stats['5gram'], (['<START>',] * (4 - i)) + words[:i+1])
        self.info['stats'] = stats

def ngram(stat, words):
    n = len(words)
    if n > 1:
        if not words[0] in stat:
            stat[words[0]] = {}
        ngram(stat[words[0]], words[1:])
    else:
        if not words[0] in stat:
            stat[words[0]] = 1
        else:
            stat[words[0]] += 1

