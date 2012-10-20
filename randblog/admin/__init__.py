from randblog.rss.admin import command as rss_command
from randblog.rss.feed import Feed
from randblog.generator.core import generate_text

#TODO: Split up into better names
def global_command(args):
    if args[0] == 'stats':
        global_stats(args[1:])
    elif args[0] == 'generate':
        global_generate(args[1:])
    else:
        print "Valid commands: stats, generate"

def global_stats(args):
    stats = Feed.stats()
    if len(args) > 0:
        with open(args[0], 'w') as out:
            import json
            json.dump(stats, out)

def global_generate(args):
    n = None

    if len(args) > 0:
        n = int(args[0])

    print generate_text(n)



