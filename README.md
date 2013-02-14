randblog
========

The Randomly Generated Blog Engine


The idea for this came from the hilarious story (and output) of Scigen, which is a CS research paper generator.
Since I started with this, I've learned of MathGen, which is a generator of Mathematics research papers.
`randblog` expands this to a new format: blogging. The idea is to continually follow technology news and generate
pseudo-sensical news articles from them.

The current software is a combination of Python and Ruby. The Python part uses `gevent`, `feedparser`, `bs4`, `pymongo`, and `mongoengine`
to follow the RSS feeds of sites, parse the entries for article text, extract word usage (n-gram) statistics from the entry
text, generate candidate articles, and store the whole thing in a MongoDB database. The Ruby/Rails part is still in early stages of
development, but will mainly be used for administrative tasks, like approving articles and OAuth authorization to a blogger account.


