from randblog.rss.feed import Feed
from gevent.pool import Pool
from gevent import sleep
from datetime import datetime
pool = Pool()

def get_feeds(args):
    if not args.feed:
        return Feed.find()
    else:
        return map(Feed.get, args.feed)

def update(args):
    print "Starting Update", datetime.now()
    if not args.feed:
        feeds = Feed.find()
    else:
        feeds = [Feed.get(f) for f in args.feed]
    do_task_for_feeds(Feed.update, get_feeds(args))
    print "Finished Update", datetime.now()

def listen(args):
    while True:
        pool.spawn(update, args)
        sleep(args.interval)


def feed_add(args):
    Feed.add(args.name, args.url)

def feed_clean_actions_show(args):
    for feed in get_feeds(args):
        print feed.name
        if 'clean_actions' in feed.info:
            for action in feed.info['clean_actions']:
                print ' -', action['task'], action['selector']

def feed_clean_actions_add(args):
    f = Feed.get(args.feed)
    if not 'clean_actions' in f.info:
        f.info['clean_actions'] = []
    f.info['clean_actions'].append({'selector': args.selector, 'task':args.action})
    f.save()

def feed_clean(args):
    do_task_for_feeds(Feed.clean, get_feeds(args))

def feed_stats(args):
    do_task_for_feeds(Feed.stats_collect, get_feeds(args))

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
    parser_update.set_defaults(func=update)
    
    # rss listen <interval> [<feed> ...]
    parser_listen = subparsers.add_parser('listen', help='Update RSS Feeds')
    parser_listen.add_argument('interval', type=int, help='Update interval')
    parser_listen.add_argument('feed', nargs='*', help='Feed to listen to')
    parser_listen.set_defaults(func=listen)

    # rss feed
    parser_feed = subparsers.add_parser('feed', help='RSS Feed Manipulation')

    subparsers_feed = parser_feed.add_subparsers(help='Feed sub-command help')

    # rss feed add <name> <url>
    parser_feed_add = subparsers_feed.add_parser('add', help='Add new RSS Feed')
    parser_feed_add.add_argument('name', help='Name of feed to add')
    parser_feed_add.add_argument('url', help='URL of feed to add')
    parser_feed_add.set_defaults(func=feed_add)

    # rss feed clean_actions
    parser_feed_clean_actions = subparsers_feed.add_parser('clean_actions', help='Manipulate Feed Entry clean directives')
    subparsers_feed_clean_actions = parser_feed_clean_actions.add_subparsers(help='Feed Clean Actions sub-command help')
    
    # rss feed clean_actions show [<feed> ...]
    parser_feed_clean_actions_show = subparsers_feed_clean_actions.add_parser('show', help='Show Feed Entry Clean Actions')
    parser_feed_clean_actions_show.add_argument('feed', nargs='*', help='Name of feed to show')
    parser_feed_clean_actions_show.set_defaults(func=feed_clean_actions_show)

    # rss feed clean_action add <feed> <selector> <action>
    parser_feed_clean_actions_add = subparsers_feed_clean_actions.add_parser('add', help='Add new Feed Entry Clean Action')
    parser_feed_clean_actions_add.add_argument('feed', help='Name of feed to edit')
    parser_feed_clean_actions_add.add_argument('selector', help='Selector to use')
    parser_feed_clean_actions_add.add_argument('action', help='Action to take')
    parser_feed_clean_actions_add.set_defaults(func=feed_clean_actions_add)

    # rss feed clean [<feed> ...]
    parser_feed_clean = subparsers_feed.add_parser('clean', help='Clean Entries for the given Feeds')
    parser_feed_clean.add_argument('feed', nargs='*', help='Name of feed to clean')
    parser_feed_clean.set_defaults(func=feed_clean)

    # rss feed stats [<feed> ...]
    parser_feed_stats = subparsers_feed.add_parser('stats', help='Generate Stats for the given Feeds')
    parser_feed_stats.add_argument('feed', nargs='*', help='Name of feed to examine')
    parser_feed_stats.set_defaults(func=feed_stats)

