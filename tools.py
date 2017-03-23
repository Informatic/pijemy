#-*- coding:utf-8 -*-

import re, shlex

def timedict(obj):
    return {'year':obj.year, 'month':obj.month, 'day':obj.day}

def render_event(evt):
    d = {
        u'Urodzili się': lambda x: u'Urodził się '+x, # if shlex.split(x)[0].endswith('a') else u'Urodził się '+x,
        'Zmarli': lambda x: u'Zmarł '+x,
    }

    for key, func in d.items():
        if key.lower() in evt[0].lower():
            return func(evt[2])
    return evt[2]

def cleanup_html(s):
    s = re.sub('\<(.+?)\>', '', s)
    s = re.sub('\&(.+?)\;', '', s)

    return s
