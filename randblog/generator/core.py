from randblog.rss.feed import Feed
from randblog.generator import output_collection
import datetime
import random

def generate_text(n):
    stats = Feed.stats(False)

    generated = {}

    if n is None:
        generated['type'] = 'multi_nGram'
        generated['text'] = generate_multi_nGram_text(stats)
    else:
        generated['type'] = 'fixed_nGram'
        generated['nGram'] = n
        generated['text'] = generate_nGram_text(stats, n)
    generated['date'] = list(datetime.datetime.now().timetuple())

    output_collection.insert(generated)
    return generated['text']

def generate_nGram_text(stats, n):
    nStats = stats.nGram(n)
    words = ['<START>'] * (n - 1)

    curr = pickWord(nStats, words)

    while curr != '<END>':
        words.append(curr)
        curr = pickWord(nStats, words[len(words) - (n - 1):])

    words = words[n-1:]

    return join_word_list(words)

def generate_multi_nGram_text(stats):
    words = ['<START>'] * 4

    curr = pickWordMulti(stats, words, 5)
    while curr != '<END>':
        words.append(curr)
        curr = pickWordMulti(stats, words[len(words) - 4:], 5)

    words = words[4:]
    return join_word_list(words)

def pickWord(stats, prevWords):
    s = stats
    for w in prevWords:
        s = s[w]
    choices = []
    for word, count in s.items():
        choices += [word] * count
    return random.choice(choices)

def pickWordMulti(stats, prevWords, maxN):
    choices = {}
    wChoices = []
    for n in range(2, maxN+1):
        s = stats.nGram(n)
        found = True
        for w in prevWords[maxN - n:]:
            if not w in s:
                found = False
                break
            s = s[w]
        if found:
            choices[n] = s

    for n in range(2, maxN+1):
        if n in choices:
            s = choices[n]
            for word, count in s.items():
                wChoices += ([word] * (count * (n - 1)**4))

    if len(wChoices) == 0:
        return '<END>'
    return random.choice(wChoices)

def join_word_list(words):
    return ' '.join(map(lambda s: s.replace('<period>', '.').replace('<dollar>', '$'), words))

