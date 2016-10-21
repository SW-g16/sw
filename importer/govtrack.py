import os
from pprint import pprint
from os import walk
import json
import sys

import requests

vote_keys = ['Yea','Nay','Not Voting']
semantic_vote_properties = [':votesYay',':votesNay',':abstain']
sessions_per_data_unload = 1
root = 'govtrack-data/data/congress/'

def int_only_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_dirnames(path):
    for (dirpath, dirnames, filenames) in walk(path): return dirnames

def get_int_folders(path):
    try:
        return sorted([int(d) for d in get_dirnames(path) if int_only_str(d)])
    except:
        print 'fuck',path


def loadJson(path):

    f = open(path)
    r = json.load(f)
    f.close()
    return r

def process_session(session_id):
    triples = []
    print "Session #",session_id
    hr_bills = get_dirnames('%s%d/bills/hr' % (root, session_id))
    s_bills = get_dirnames('%s%d/bills/s' % (root, session_id))
    vote_subdirs = get_int_folders('%s%d/votes' % (root, session_id))
    for v_subdir in vote_subdirs:
        votes = get_dirnames('%s%d/votes/%d' % (root, session_id , v_subdir))
        for v in votes:
            if v[0]!='s' and v[0]!='h': continue
            data_path = '%s%d/votes/%d/%s/data.json' % (root, session_id , v_subdir, v)
            bill_data = loadJson(data_path)

            #vote_event_uri = '<gt_vote_event#%d>' % bill_data['vote_id']
            bill_uri = '<gt_bill#%d>' % bill_data['number']
            # bill_text =

            #sys.stdout.write('.')

            for k in range(0,3):
                if 'votes' not in bill_data or vote_keys[k] not in bill_data['votes']:
                    continue
                for vote in bill_data['votes'][vote_keys[k]]:
                    #party_uri = nay['party']
                    #state = nay['state']
                    voter_uri = '<gt_voter#%s>' % vote['id']
                    triples.append((voter_uri,semantic_vote_properties[k],bill_uri))

    return triples

def constructData():

    session_uris = get_int_folders(root)

    triples = []

    i = 0

    for session_id in session_uris:
        triples += process_session(session_id)
        i += 1
        if i % sessions_per_data_unload == 0:
            s = ''
            for t in triples:
                s += "%s %s %s .\n" % t
            print s
            print requests.post('http://localhost:5000/store',data={'data':s})
            triples = []

    return True