import sys

from randblog.admin import *

if __name__ == '__main__':
    print sys.argv[1:]
    if sys.argv[1] == 'rss':
        rss_command(sys.argv[2:])
    elif sys.argv[1] == 'global':
        global_command(sys.argv[2:])

