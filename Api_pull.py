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
    count = 1
    headers = {}
    plyr_database = 'player_data.sqlite'
    conn = sqlite3.connect(plyr_database)
    c = conn.cursor()
    response1 = {}
    response2 = {}
    while count < 700:
        link = 'http://fantasy.premierleague.com/web/api/elements/'+str(count)+'/'
        req     = urllib2.Request(link,headers=headers)
        response = json.loads(urllib2.urlopen(req).read(),object_hook=ascii_encode_dict)
        first_val= response['first_name']+response['second_name']+response['team_name']
        json_to_plyrInfo(response, response1, first_val, count, c)
        json_to_plyrStats(response, response2, first_val, count, c)
        json_to_plyrFixture(response, response2, first_val, count, c)
        count += 1
    conn.commit()
    conn.close()
    print (time.time() - start_time())

def json_to_plyrInfo(response, response1 , first_val, count, c):
    for keys in response:
        if not (isinstance(response[keys], dict) or isinstance(response[keys], list) or isinstance(response[keys], tuple)):
            response1[keys] = response[keys]
    resp1_keys   = response1.keys()
    resp1_keys.append('Player')
    resp1_values = response1.values()
    resp1_values.append(first_val)
    if count == 1:
        c.execute('DROP TABLE IF EXISTS player_info')
        first_col    = 'Player'
        field_type   = 'TEXT'
        c.execute('CREATE TABLE player_info ({fc} {ft} PRIMARY KEY)'\
                   .format(fc=first_col, ft=field_type))
        for keys in response1:
            alter_query  = "ALTER TABLE player_info ADD COLUMN '%s' TEXT" %keys
            c.execute(alter_query)
    insert_query = 'INSERT INTO player_info (%s) VALUES (%s)'%(",".join(resp1_keys),",".join(['?']*len(resp1_keys)))
    c.execute(insert_query,resp1_values)


def json_to_plyrStats(response, response2, first_val, count, c):
    for keys in response:
        if (isinstance(response[keys], dict) or isinstance(response[keys], list) or isinstance(response[keys], tuple)):
            response2 = response["fixture_history"]["all"]
    resp1_keys   = ['Date','Round','Opponent','Mins_plyd','Goals_scrd','Assists','clean_sheet','Goal_conc','Own_goals','Pnlts_saved',\
                    'Pnlts_misd','yelw_crd','red_crd','Saves','Bonus','Ea_ppi','Bnus_pt_sys','Net_trnsfrs','Val','Total']
    if count == 1:
        c.execute('DROP TABLE IF EXISTS player_stats')
        first_col    = 'Player'
        field_type   = 'TEXT'
        c.execute('CREATE TABLE player_stats ({fc} {ft})'\
                   .format(fc=first_col, ft=field_type))
        for cols in resp1_keys:
            alter_query  = "ALTER TABLE player_stats ADD COLUMN '%s' TEXT" %cols
            c.execute(alter_query)
    resp1_keys.insert(0,'Player')
    for rounds in response2:
        rounds.insert(0,first_val)
        insert_query = 'INSERT INTO player_stats (%s) VALUES (%s)'%(",".join(resp1_keys),",".join(['?']*len(resp1_keys)))
        c.execute(insert_query,rounds)

def json_to_plyrFixture(response, response2, first_val, count, c):
    for keys in response:
        if (isinstance(response[keys], dict) or isinstance(response[keys], list) or isinstance(response[keys], tuple)):
            response2 = response["fixtures"]["all"]
    resp1_keys   = ['Date','Game_week','Opponent']
    if count == 1:
        c.execute('DROP TABLE IF EXISTS player_fixture')
        first_col    = 'Player'
        field_type   = 'TEXT'
        c.execute('CREATE TABLE player_fixture ({fc} {ft})'\
                   .format(fc=first_col, ft=field_type))
        for cols in resp1_keys:
            alter_query  = "ALTER TABLE player_fixture ADD COLUMN '%s' TEXT" %cols
            c.execute(alter_query)
    resp1_keys.insert(0,'Player')
    for rounds in response2:
        rounds.insert(0,first_val)
        insert_query = 'INSERT INTO player_fixture (%s) VALUES (%s)'%(",".join(resp1_keys),",".join(['?']*len(resp1_keys)))
        c.execute(insert_query,rounds)

api_data ()
