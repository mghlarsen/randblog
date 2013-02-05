from mongoengine import *

def convert_time_tuple(t):
   return datetime.fromtimestamp(mktime(t))

class FeedCleanAction(EmbeddedDocument):
    meta = {'allow_inheritance':False}
    task = StringField(required=True)
    selector = StringField(required=True)
    contains_text = StringField()
    match_text = StringField()

class FeedStatus(EmbeddedDocument):
    meta = {'allow_inheritance':False}
    updated = DateTimeField()
    etag = StringField()
    modified = DateTimeField()
    version = StringField()
    encoding = StringField()
    

class Feed(Document):
    name = StringField(required=True)
    title = StringField()
    subtitle = StringField()
    url = StringField(required=True)
    link = StringField()
    status = EmbeddedDocumentField(FeedStatus)
    clean_actions = ListField(EmbeddedDocumentField(FeedCleanAction))

    def update(self, update = True):
        self._feed_load(update)

    def _feed_load(self, update = False):
        feed = self._get_feed(update)
        if not feed is None:
            from randblog.rss.entry_engine import Entry
            print "Feed Data Modified"
            self.status.version = feed.version
            self.status.encoding = feed.encoding
            if hasattr(feed, 'etag'):
                self.status.etag = feed.etag
            if hasattr(feed, 'updated_parsed'):
                self.status.updated = convert_time_tuple(self._feed.updated_parsed)
            if hasattr(feed, 'modified_parsed'):
                self.status.modified = convert_time_tuple(self._feed.modified_parsed)

            for e_data in feed.entries:
                e, created = Entry.objects.get_or_create(feed=self, entry_id=e_data['id'])
                for key, value in e_data.items():
                    if key in ('updated', 'modified', 'published'):
                        pass
                    elif key == 'updated_parsed':
                        e.updated = convert_time_tuple(value)
                    elif key == 'modified_parsed':
                        e.modified = convert_time_tuple(value)
                    elif key == 'published_parsed' and created:
                        e.published = convert_time_tuple(value)
                    else:
                        setattr(e, key, value)
                if created and e.published is None:
                    e.published = datetime.datetime.now()
                e.save()

def convert_old_feeds():
    from randblog.rss.feed import Feed as OldFeed
    from randblog.rss.entry_engine import Entry
    from randblog.crawler.link_engine import Link
    from randblog.corpus.item_engine import CorpusItem
    for f in OldFeed.find():
        print f.name
        feed, created = Feed.objects.get_or_create(name=f.name, url=f.url)
        print "CREATED:", created
        if 'title' in f.info:
            feed.title = f.title
        if 'subtitle' in f.info:
            feed.subtitle = f.subtitle
        if 'link' in f.info:
            feed.link = f.link
        if 'status' in f.info:
            feed.status = FeedStatus(**f.info['status'])
        if 'clean_actions' in f.info:
            feed.clean_actions = []
            for action in f.info['clean_actions']:
                feed.clean_actions.append(FeedCleanAction(**action))
        feed.save()
        f._db_entries_load()
        for entry_id, e in f.entries.items():
            print entry_id
            entry, e_created = Entry.objects.get_or_create(feed = feed, entry_id = entry_id, defaults={'title':e.info['title']})
            print "CREATED:", e_created
            if 'title' in e.info:
                entry.title = e.info['title']
            if 'link' in e.info:
                entry.link = e.link
            entry.save()
