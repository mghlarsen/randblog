from randblog.corpus.item import Item
from randblog.rss.feed import Feed

def extract(args):
    i = 0

    for item in Item.find():
        print item._data['title'], item.extract_crawl_links()
        i+=1
        print i, "done"
        if args.n and args.n <= i:
            return

def stats(args):
    stats = Feed.stats()

def setup_parser(sp):
    parser = sp.add_parser('corpus', help='Corpus commands')
    subparsers = parser.add_subparsers(help='Corpus sub-command help')

    # corpus stats
    parser_stats = subparsers.add_parser('stats', help='extract stats from corpus')
    parser_stats.set_defaults(func=stats)

    # corpus extract
    parser_extract = subparsers.add_parser('extract', help='extract links from corpus items for crawling')
    parser_extract.add_argument('n', type=int, nargs='?', help='Number of extractions to make')
    parser_extract.set_defaults(func=extract)

