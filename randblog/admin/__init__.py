from randblog.rss.feed import Feed
from gevent.pool import Pool
import random
pool = Pool()

from randblog.rss.admin import command as rss_command

#TODO: Split up into better names
def global_command(args):
    if args[0] == 'stats':
        global_stats(args[1:])
    elif args[0] == 'generate':
        global_generate(args[1:])

def global_stats(args):
    stats = Feed.stats()
    if len(args) > 0:
        with open(args[0], 'w') as out:
            import json
            json.dump(stats, out)

def global_generate(args):
    stats = Feed.stats(False)
    n = None

    if len(args) > 0:
        n = int(args[0])

    if not n is None:
        nStats = stats[str(n) + 'gram']
        words = ['<START>'] * (n - 1)

        curr = pickWork(nStats, words)

        while curr != '<END>':
            words.append(curr)
            curr = pickWord(nStats, words[len(words) - (n - 1):])

        words = words[n-1:]
    else:
        words = ['<START>'] * 4

        curr = pickWordMulti(stats, words, 5)
        while curr != '<END>':
            words.append(curr)
            curr = pickWordMulti(stats, words[len(words) - 4:], 5)

        words = words[4:]

    print ' '.join(map(lambda s: s.replace('<period>', '.').replace('<dollar>', '$'), words))

def do_task_for_feeds(task, feeds):
    for res in pool.map(task, feeds):
        if not res is None and not isinstance(res, dict):
            res.join()
            print res.value

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
        s = stats[str(n) + 'gram']
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


