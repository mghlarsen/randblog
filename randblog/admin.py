import sys

if __name__ == '__main__':
    print sys.argv[1:]
    if sys.argv[1] == 'feed':
        from randblog.rss.feed import Feed
        if sys.argv[2] == 'add':
            Feed.add(sys.argv[3], sys.argv[4])
        if sys.argv[2] == 'update':
            if len(sys.argv) > 3 and sys.argv[3] == 'False':
                update = False
            else:
                update = True

            from gevent.pool import Pool
            p = Pool()
            feeds = Feed.find()
            for res in p.map(lambda f: f.update(), feeds):
                if not res is None:
                    res.join()
                    print res.value
 
