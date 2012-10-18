import sys

from randblog.admin import *

if __name__ == '__main__':
    print sys.argv[1:]
    if sys.argv[1] == 'feed':
        if sys.argv[2] == 'add':
            Feed.add(sys.argv[3], sys.argv[4])
        elif sys.argv[2] == 'update':
            if len(sys.argv) > 3 and sys.argv[3] == 'False':
                update = False
            else:
                update = True

            feeds = Feed.find()
            do_task_for_feeds(lambda f: f.update(), feeds)
        elif sys.argv[2] == 'clean_actions':
            if sys.argv[3] == 'show':
                if len(sys.argv) > 4:
                    feeds = [Feed.get(sys.argv[4])]
                else:
                    feeds = Feed.find()
                for feed in feeds:
                    print feed.name
                    if 'clean_actions' in feed.info:
                        for action in feed.info['clean_actions']:
                            print ' -', action['task'], action['selector']

            elif sys.argv[3] == 'add':
                f = Feed.get(sys.argv[4])
                if not 'clean_actions' in f.info:
                    f.info['clean_actions'] = []
                f.info['clean_actions'].append({'selector': sys.argv[5], 'task': sys.argv[6]})
                f.save()
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
