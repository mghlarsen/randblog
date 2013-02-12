from randblog.rss import convert_time_tuple
import feedparser
from datetime import datetime
from mongoengine import *

__all__ = ['Feed', 'FeedStatus', 'FeedCleanAction']

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
            from randblog.rss.entry import Entry
            import randblog.corpus.item
            import randblog.crawler.link
            print "Feed Data Modified"
            self.status.version = feed.version
            self.status.encoding = feed.encoding
            if hasattr(feed, 'etag'):
                self.status.etag = feed.etag
            if hasattr(feed, 'updated_parsed'):
                self.status.updated = convert_time_tuple(feed.updated_parsed)
            if hasattr(feed, 'modified_parsed'):
                self.status.modified = convert_time_tuple(feed.modified_parsed)

            for e_data in feed.entries:
                e, created = Entry.objects.get_or_create(feed=self, entry_id=e_data['id'], defaults = {'title':e_data['title']})
                e.populate_from_dict_info(e_data)
                if created and e.published is None:
                    e.published = datetime.utcnow()
                e.save()
                e.clean()

    def _get_feed(self, update = False):
        if update and (not self.status is None):
            opts = {}
            if not self.status is None:
                if self.status.etag:
                    opts['etag'] = self.status.etag
                if self.status.modified:
                    opts['modified'] = self.status.modified
            feed = feedparser.parse(self.url, **opts)
            if feed.status == 304:
                return None
        elif self.status is None:
            feed = feedparser.parse(self.url)
        return feed

