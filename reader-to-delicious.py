#!/usr/bin/env python

try:
    import json
except ImportError:
    import simplejson as json

import re
import time
import datetime
from getpass import getpass
import pprint
import pydelicious

ADD_TAG = '_from:greader'

#SLICE = slice(0,1)  # for just the first item
#SLICE = slice(3,5)  # for the 4th and 5th items
SLICE = slice(None)  # for all items

REPLACE_IF_EXISTS = False
SHARED = False
RE_TAG = re.compile(r'user/\d+/label/(.+)')
SLEEP_INTERVAL = 3


def tags_from_categories(categories):
    tags = []
    for cat in categories:
        m = RE_TAG.match(cat)
        if m:
            tags.append(m.group(1))
    return tags


def prepare_item(item):
    assert len(item['alternate']) == 1, item['title'] + item['alternate']
    url = item['alternate'][0]['href']

    # Google doesn't seem to save the time that I starred the items, so
    # crawlTimeMsec is the closest estimate
    crawltime_sec = int(item['crawlTimeMsec']) / 1000
    dt = datetime.datetime.utcfromtimestamp(crawltime_sec)

    # sometimes there's no title, take the original feed title
    title = item.get('title', item['origin']['title'])
    comments = '\n'.join(item['comments'])
    tags = tags_from_categories(item['categories'])
    if tags:
        print title, tags
    if ADD_TAG:
        tags.append(ADD_TAG)

    assert url
    assert title

    if comments:
        print item['title'], "comment =", comments

    return dict(
        url=url,
        description=title,
        extended=comments,
        tags=','.join(tags),
        dt=dt.strftime('%Y-%m-%dT%H:%M:%SZ'),
        replace=REPLACE_IF_EXISTS,
        shared=SHARED,
    )


def main(duser, dpass, filename):
    with open(filename) as f:
        starred = json.load(f)

    print "importing", len(starred['items'][SLICE]), "items"
    for i, item in enumerate(starred['items'][SLICE]):
        kwargs = prepare_item(item)
        api = pydelicious.apiNew(duser, dpass)
        try:
            api.posts_add(**kwargs)
        except pydelicious.DeliciousItemExistsError:
            print "Item", i, "already exists:", kwargs['description']
            pprint.pprint(kwargs)
        except Exception, e:
            print "item ", i, "failed"
            pprint.pprint(kwargs)
            print e

        time.sleep(SLEEP_INTERVAL)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print >> sys.stderr, "Usage: %s <delicious_username> <path to starred.json>"
        sys.exit(1)

    duser, filename = sys.argv[1:]

    while True:
        try:
            dpass = getpass("Delicious password: ")
        except EOFError:
            dpass = ''
        dpass = dpass.strip()
        if dpass:
            break
        print >> sys.stderr, "no password entered!"

    main(duser, dpass, filename)
