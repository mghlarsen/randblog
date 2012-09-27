import sys
from randblog.rss.feed import Feed
from gevent.pool import Pool
import random
pool = Pool()

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
    choices = []
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
            choices.append((n, s))

    for n, s in choices:
        for word, count in s.items():
            wChoices += ([word] * (count * (n - 1)**4))
        if n - 2 == len(choices) and n != maxN:
            for word, count in s.items():
                wChoices += ([word] * (count * maxN**4))

    if len(wChoices) == 0:
        return '<END>'
    return random.choice(wChoices)

if __name__ == '__main__':
    print sys.argv[1:]
    if sys.argv[1] == 'feed':
        if sys.argv[2] == 'add':
            Feed.add(sys.argv[3], sys.argv[4])
        if sys.argv[2] == 'update':
            if len(sys.argv) > 3 and sys.argv[3] == 'False':
                update = False
            else:
                update = True

            feeds = Feed.find()
            do_task_for_feeds(lambda f: f.update(), feeds)
    elif sys.argv[1] == 'entry':
        if sys.argv[2] == 'clean':
            if len(sys.argv) == 3:
                toClean = Feed.find()
            else:
                toClean = [Feed.get(f) for f in sys.argv[3:]]
            
            do_task_for_feeds(lambda f: f.clean(), toClean)

        elif sys.argv[2] == 'stats':
            if len(sys.argv) == 3:
                toStat = Feed.find()
            else:
                toStat = [Feed.get(f) for f in sys.argv[3:]]

            do_task_for_feeds(lambda f: f.stats_collect(True), toStat)
    elif sys.argv[1] == 'global':
        if sys.argv[2] == 'stats':
            stats = Feed.stats()
            if len(sys.argv) > 3:
                with open(sys.argv[3], 'w') as out:
                    import json
                    out.write(json.dumps(stats))
        elif sys.argv[2] == 'generate':
            stats = Feed.stats(False)
            n = None

            if len(sys.argv) > 3:
                n = int(sys.argv[3])
            
            if not n is None:
                nStats = stats[str(n) + 'gram']
                words = ['<START>'] * (n - 1)
    
                curr = pickWord(nStats, words)

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
