from randblog.rss.feed import Feed
from gevent.pool import Pool
import random
pool = Pool()

def feed_command(args):
    if args[0] == 'add':
        feed_add(args[1:])
    elif args[0] == 'update':
        feed_update(args[1:])
    elif args[0] == 'clean_actions':
        feed_clean_actions(args[1:])

def feed_add(args):
    Feed.add(args[0], args[1])

def feed_update(args):
    if len(args) > 0 and args[0] == 'False':
        update = False
    else:
        update = True

    feeds = Feed.find()
    do_task_for_feeds(Feed.update, feeds)

def feed_clean_actions(args):
    if args[0] == 'show':
        feed_clean_actions_show(args[1:])
    elif args[0] == 'add':
        feed_clean_actions_add(args[1:])

def feed_clean_actions_show(args):
    if len(args) > 0:
        feeds = [Feed.get(args[0])]
    else:
        feeds = Feed.find()

    for feed in feeds:
        print feed.name
        if 'clean_actions' in feed.info:
            for action in feed.info['clean_actions']:
                print ' -', action['task'], action['selector']

def feed_clean_actions_add(args):
    f = Feed.get(args[0])
    if not 'clean_actions' in f.info:
        f.info['clean_actions'] = []
    f.info['clean_actions'].append({'selector': args[1], 'task':args[2]})
    f.save()

def entry_command(args):
    if args[0] == 'clean':
        entry_clean(args[1:])
    elif args[0] == 'stats':
        entry_stats(args[1:])

def entry_clean(args):
    if len(args) > 0:
        toClean = [Feed.get(f) for f in args]
    else:
        toClean = Feed.find()
    do_task_for_feeds(Feed.clean, toClean)

def entry_stats(args):
    if len(args) > 0:
        toStat = [Feed.get(f) for f in args]
    else:
        toStat = Feed.find()
    do_task_for_feeds(Feed.stats_collect, toStat)

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


