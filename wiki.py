#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import re
import datetime
import os
import tools
import pickle

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cache', '%(year)s', '%(month)s', '%(day)s.cache')

def get_page(article):
    return urllib.urlopen("http://pl.wikipedia.org/w/index.php?title=%s&action=raw" % (urllib.quote(article),)).read()

def get_events_page(date):
    if date == None:
        date = datetime.datetime.now()

    months = ['stycznia', 'lutego', 'marca', 'kwietnia', 'maja', 'czerwca', 'lipca', 'sierpnia', 'września', 'października', 'listopada', 'grudnia']

    return get_page( "%d_%s" % (date.day, months[date.month-1]) )

def parse_events_page(article):
    results = []
    for section in re.findall('\=\= (.*?) \=\=\n(.*?)\n\n', article, re.DOTALL):
        print('section', section)
        for result in re.findall('\* \[\[(\d*)\]\][:– *\n]+(.*?)\s\* \[\[', section[1], re.DOTALL):
            print('result', result)
            for rec in [re.sub('\[\[(.*?)\]\]', '\\1', re.sub('\[\[([^]]*?)\|(.*?)\]\]', '\\2', rec)) for rec in result[1].split('\n** ')]:
                print('rec', rec)
                results.append((section[0].decode('utf-8'), result[0], tools.cleanup_html(rec.decode('utf-8'))))

    return results

def get_events(date=None):
    return parse_events_page(get_events_page(date))

def get_events_cached(date=None):
    if date == None:
        date = datetime.datetime.now()

    cachefile = CACHE_PATH % tools.timedict(date)
    if os.path.exists(cachefile):
        return pickle.loads(open(cachefile).read())

    data = get_events(date)

    if not os.path.exists(os.path.dirname(cachefile)):
        os.makedirs(os.path.dirname(cachefile))
    with open(cachefile, 'w+') as fd:
        fd.write(pickle.dumps(data))

    return data

if __name__ == '__main__':
    print(get_events(datetime.datetime.now()))
