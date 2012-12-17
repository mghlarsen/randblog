from randblog.rss.admin import setup_parser as rss_setup_parser
from randblog.corpus.admin import setup_parser as corpus_setup_parser
from randblog.generator.core import generate_text

import argparse

parser = argparse.ArgumentParser(prog='randblog')

subparsers = parser.add_subparsers(help = 'sub-command help')

def generate(args):
    if args.n:
        print generate_text(args.n)
    else:
        print generate_text(None)

parser_generate = subparsers.add_parser('generate', help='generate text from stats')
parser_generate.add_argument('n', type=int, nargs='?', help='n parameter for nGram generator (leaving blank make it variable)')
parser_generate.set_defaults(func=generate)

rss_setup_parser(subparsers)
corpus_setup_parser(subparsers)
