from randblog.corpus import stats_collection, word_encode

MAX_NGRAM = 5
def ngram_range():
    return range(2, MAX_NGRAM + 1)

class Stats(object):
    def __init__(self, name, info = {}):
        self._data = {}
        query = {}
        query.update(info)
        query['name'] = name
        self._info = query
        for piece in stats_collection.find(query):
            self._data[int(piece['gramLen'])] = piece
        for n in ngram_range():
            if not n in self._data:
                self._data[n] = {'gramLen':n}
                self._data[n].update(self._info)

    def get_ids(self):
        ids = []
        for n in ngram_range():
            if '_id' in self._data[n]:
                ids.append(self._data[n]['_id'])
        ids.sort()
        return ids

    def save(self):
        for n, data in self._data.items():
            stats_collection.save(data)

    def nGram(self, n):
        if not 'data' in self._data[n]:
            self._data[n]['data'] = {}
        return self._data[n]['data']

    def collect_words(self, words):
        curr_words = ['<START>'] * 4
        for word in (word_encode(word) for word in words):
            curr_words.append(word)
            curr_words = curr_words[len(curr_words)-MAX_NGRAM:]
            self._update_ngrams(curr_words)
        curr_words.append('<END>')
        curr_words = curr_words[len(curr_words) - MAX_NGRAM:]
        self._update_ngrams(curr_words)

    def _update_ngrams(self, words):
        for i in ngram_range():
            self._add_ngram(i, self.nGram(i), words[MAX_NGRAM - i:])

    def _add_ngram(self, n, stat, words):
        assert n == len(words)
        if n > 1:
            if not words[0] in stat:
                stat[words[0]] = {}
            self._add_ngram(n-1, stat[words[0]], words[1:])
        else:
            if words[0] in stat:
                stat[words[0]] += 1
            else:
                stat[words[0]] = 1

    def clear(self):
        for n in ngram_range():
            self._data[n]['data'] = {}

    def aggregate(self, query):
        for piece in stats_collection.find(query):
            n = piece['gramLen']
            new = piece['data']
            curr = self.nGram(n)
            self._agg_ngram(curr, new, n)

    def _agg_ngram(self, curr, new, n):
        for key, value in new.items():
            if not key in curr:
                curr[key] = value
            elif n > 1:
                self._agg_ngram(curr[key], value, n - 1)
            else:
                curr[key] += value
