from randblog.rss.admin import setup_parser as rss_setup_parser
from randblog.rss.feed import Feed
from randblog.generator.core import generate_text

import argparse

parser = argparse.ArgumentParser(prog='randblog')

subparsers = parser.add_subparsers(help = 'sub-command help')

parser_global_stats = subparsers.add_parser('stats', help='extract stats from corpus')
parser_global_generate = subparsers.add_parser('generate', help='generate text from stats')

def global_stats(args):
    stats = Feed.stats()
    if len(args) > 0:
        with open(args[0], 'w') as out:
            import json
            json.dump(stats, out)
parser_global_stats.set_defaults(func=global_stats)

def global_generate(args):
    n = None

    if len(args) > 0:
        n = int(args[0])

    print generate_text(n)
parser_global_generate.set_defaults(func=global_generate)

rss_setup_parser(subparsers)
