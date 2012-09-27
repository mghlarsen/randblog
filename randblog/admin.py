import sys
from randblog.rss.feed import Feed
from gevent.pool import Pool
pool = Pool()

def do_task_for_feeds(task, feeds):
    for res in pool.map(task, feeds):
        if not res is None and not isinstance(res, dict):
            res.join()
            print res.value

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
            with open(sys.argv[3], 'w') as out:
                import json
                out.write(json.dumps(Feed.stats()))

