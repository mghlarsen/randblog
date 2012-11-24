from randblog.rss.admin import setup_parser as rss_setup_parser
from randblog.rss.feed import Feed
from randblog.generator.core import generate_text

import argparse

parser = argparse.ArgumentParser(prog='randblog')

subparsers = parser.add_subparsers(help = 'sub-command help')


def stats(args):
    stats = Feed.stats()

def generate(args):
    if args.n:
        print generate_text(n)
    else:
        print generate_text(None)

parser_stats = subparsers.add_parser('stats', help='extract stats from corpus')
parser_stats.set_defaults(func=stats)

parser_generate = subparsers.add_parser('generate', help='generate text from stats')
parser_generate.add_argument('n', type=int, nargs='?', help='n parameter for nGram generator (leaving blank make it variable)')
parser_generate.set_defaults(func=generate)

rss_setup_parser(subparsers)
