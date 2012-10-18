from randblog.rss.feed import Feed

def command(args):
    if args[0] == 'add':
        feed_add(args[1:])
    elif args[0] == 'update':
        feed_update(args[1:])
    elif args[0] == 'clean_actions':
        feed_clean_actions(args[1:])
    elif args[0] == 'entry':
        feed_entry_command(args[1:])

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

def feed_entry_command(args):
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


