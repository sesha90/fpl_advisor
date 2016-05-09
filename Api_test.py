import sqlite3
import sys
import json
import urllib2
import types
import time

def ascii_encode_dict(data):
    ascii_encode = lambda x: x.encode('ascii','ignore') if isinstance(x, unicode) else x
    return dict(map(ascii_encode, pair) for pair in data.items()) 

def api_data ():
    start_time = time.time()
    headers = {}
    count = 1
    plyr_database = 'player_data.sqlite'
    conn = sqlite3.connect(plyr_database)
    c = conn.cursor()
    link = 'http://fantasy.premierleague.com/web/api/entry/1992833/event-history/35'
    req     = urllib2.Request(link,headers=headers)
    response = json.loads(urllib2.urlopen(req).read(),object_hook=ascii_encode_dict)
    print response 
api_data ()
