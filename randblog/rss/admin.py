from randblog.rss.feed import Feed
from gevent.pool import Pool
from gevent import sleep
from datetime import datetime
pool = Pool()

def get_feeds(feed_names):
    if not feed_names:
        return Feed.objects
    else:
        return [Feed.objects.get(name = name) for name in feed_names]

def update(feed_names):
    print "Starting Update", datetime.now()
    do_task_for_feeds(Feed.update, get_feeds(feed_names))
    print "Finished Update", datetime.now()

def listen(feed_names, interval):
    while True:
        pool.spawn(update, feed_names)
        sleep(interval)

def do_task_for_feeds(task, feeds):
    for res in pool.map(task, feeds):
        if not res is None and hasattr(res, 'join'):
            res.join()
            print res.value

def setup_parser(sp):
    parser = sp.add_parser('rss', help='RSS commands')
    subparsers = parser.add_subparsers(help='RSS sub-command help')

    # rss update [<feed> ...]
    parser_update = subparsers.add_parser('update', help='Update RSS Feeds')
    parser_update.add_argument('feed', nargs='*', help='Feed to update')
    parser_update.set_defaults(func=lambda args: update(args.feed))

    # rss listen <interval> [<feed> ...]
    parser_listen = subparsers.add_parser('listen', help='Update RSS Feeds')
    parser_listen.add_argument('interval', type=int, help='Update interval')
    parser_listen.add_argument('feed', nargs='*', help='Feed to listen to')
    parser_listen.set_defaults(func=lambda args: listen(args.feed, args.interval))
