from randblog.rss.feed import Feed
from gevent.pool import Pool
pool = Pool()

def command(args):
    if args[0] == 'update':
        update(args[1:])
    elif args[0] == 'feed':
        feed(args[1:])
    else:
        print "Valid commands: update, feed"

def update(args):
    if len(args) > 0 and args[0] == 'False':
        update = False
    else:
        update = True

    feeds = Feed.find()
    do_task_for_feeds(Feed.update, feeds)

def feed(args):
    if args[0] == 'add':
        feed_add(args[1:])
    elif args[0] == 'clean_actions':
        feed_clean_actions(args[1:])
    elif args[0] == 'clean':
        feed_clean(args[1:])
    elif args[0] == 'stats':
        feed_stats(args[1:])

def feed_add(args):
    Feed.add(args[0], args[1])

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

def feed_clean(args):
    if len(args) > 0:
        toClean = [Feed.get(f) for f in args]
    else:
        toClean = Feed.find()
    do_task_for_feeds(Feed.clean, toClean)

def feed_stats(args):
    if len(args) > 0:
        toStat = [Feed.get(f) for f in args]
    else:
        toStat = Feed.find()
    do_task_for_feeds(Feed.stats_collect, toStat)

def do_task_for_feeds(task, feeds):
    for res in pool.map(task, feeds):
        if not res is None and hasattr(res, 'join'):
            res.join()
            print res.value


