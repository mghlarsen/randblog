from randblog import db
from urlparse import urlsplit, SplitResult
import re

__all__ = ['clean_link', 'link_collection']

__utm_matcher = re.compile(r'((?:^|\&)utm_[_a-z]+=[^&]*)')

ALLOWED_URL_SCHEMES = ['http', 'https']

def clean_link(url):
    o = urlsplit(url)
    if not o.scheme.lower() in ALLOWED_URL_SCHEMES:
        return None
    o = SplitResult(o.scheme, o.netloc, o.path, o.query, '')
    while o.query and __utm_matcher.search(o.query):
        query = __utm_matcher.sub('', o.query)
        o = SplitResult(o.scheme, o.netloc, o.path, query, '')
    return o.geturl()

link_collection = db['links']

