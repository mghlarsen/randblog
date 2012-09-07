import sys

if __name__ == '__main__':
    print sys.argv[1:]
    if sys.argv[1] == 'feed':
        from trgtb.rss.feed import Feed
        if sys.argv[2] == 'add':
            Feed.add(sys.argv[3], sys.argv[4])

