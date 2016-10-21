import os
import threading
from os import walk
import json
import time
import requests
import thread

MAX_ACTIVE_THREADS = 8
ROOT = 'govtrack-data/data/congress/' # the location of the downloaded bulk data, relative from where you call this script
VOTE_PROPERTIES = [':votesYay', ':votesNay', ':abstain']
VOTE_KEYS = ['Yea', 'Nay', 'Not Voting']

global thread_status_dict
global num_active_threads

thread_status_dict = {}

def get_dirnames(path):
    if not os.path.isdir(path):
        print "Dirnames of non-existing folder requested"
        return None
    try:
        for (dirpath, dirnames, filenames) in walk(path): return dirnames
    except:
        print 'Path existed but caused error: ',path
        return None

def is_int_only_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return None

def get_int_dirnames(path):
    # returns names of all directories within path
    if not os.path.isdir(path):
        print "(get_dirnames) Dirnames of non-existing folder requested"
        return None
    try:
        return sorted([int(d) for d in get_dirnames(path) if is_int_only_str(d)])
    except:
        print  '(get_int_dirnames) Path existed but caused error: ',path
        return None

def wipe_working_tags(session_ids):
    # clears all 'working' tags within the source data set
    # the tags are used to navigate worker threads
    print session_ids
    for s_id in session_ids:
        path = '%s/%d/working' % (ROOT, s_id)
        if os.path.isfile(path): os.remove(path)


def wipe_done_tags(session_ids):
    # clears all 'working' tags within the source data set
    # the tags are used to navigate worker threads
    for s_id in session_ids:
        path = '%s/%d/done' % (ROOT, s_id)
        if os.path.isfile(path): os.remove(path)

def loadJsonFile(path):
    if not os.path.isfile(path):
        print "(loadJsonfile) File doesn't exist",path
        return None
    try:
        f = open(path)
        r = json.load(f)
        f.close()
        return r
    except:
        print  '(loadJsonFile) Path existed but caused error: ',path
        return None

def mark_session(session_id,key):

    if key == 'working':
        # the thread is starting work on this branch
        # we mark it so other threads stay away from this session
        f = open("%s%d/%s" % (ROOT, session_id, key), 'w')
        f.close()
        return True
    elif key == 'done':
        # the thread is done with this branch
        # we mark it as done so other threads stay away from this session, also upon a later run of this program
        f = open("%s%d/%s" % (ROOT, session_id, key), 'w')
        f.close()
        if (os.path.isfile("%s%d/working"%(ROOT, session_id))):
            os.remove("%s%d/working" % (ROOT, session_id))

        return True

    else:
        print "invalid key: ",key
        return False


def process_session(session_id):

    triples = []


    def send_to_db(triples):
        s = '@prefix : <http://www.votes.example.com/> .\n'
        for t in triples: s += "%s %s %s .\n" % t
        print 'put %d triples in db' %len(triples)
        return requests.post('http://localhost:5000/store',data={'data':s})


    vote_groups = get_int_dirnames('%s%d/votes' % (ROOT, session_id))

    if vote_groups is None: return []

    for g in vote_groups:

        bills = get_dirnames('%s%d/votes/%d' % (ROOT, session_id , g))

        for b in bills:

            if len(triples)>10000:
                send_to_db(triples)
                triples = []

            if b[0]!='s' and b[0]!='h': continue

            bill_data = loadJsonFile('%s%d/votes/%d/%s/data.json' % (ROOT, session_id , g, b))

            if bill_data is None or 'votes' not in bill_data: continue

            # this is where to pick out bill data
            # // todo get data, bill text, vote event

            bill_uri = '<gt_bill#%d>' % bill_data['number']

            # print bill_uri

            for k in range(0,3):

                if VOTE_KEYS[k] not in bill_data['votes']: continue

                for vote in bill_data['votes'][VOTE_KEYS[k]]:

                    if vote is None: continue

                    # print vote['id']

                    # these are the 3 relevant fields about the voter from this data source
                    # csv files are available for full names, profile pictures, contact info, and more
                    # party affiliation might change over time though, so we keep the party at the time of vote
                    # // todo also get commented-out stuff
                    # party_uri = nay['party']
                    # state = nay['state']

                    voter_uri = '<gt_voter#%s>' % vote['id'] # the id of the voter who gave the vote

                    triples.append((voter_uri, VOTE_PROPERTIES[k], bill_uri))


    send_to_db(triples)

    return True

def change_num_active_threads(val):
    global num_active_threads
    num_active_threads = num_active_threads + val

def worker(s_id):

    global thread_status_dict
    global num_active_threads

    thread_status_dict[s_id] = 1

    # start = time.time()

    def fail(message):
        print message
        change_num_active_threads(-1)
        return False

    def didit():
        change_num_active_threads(-1)
        return True

    if mark_session(s_id,'working') is False: return fail('failed to set work tag %d.' % s_id )

    process_session(s_id)

    if not mark_session(s_id,'done'):
        return fail('failed to set done tag %d. ',s_id)

    # print s_id,'time:',time.time()-start

    thread_status_dict[s_id] = 2 # received stardog response
    print 'hoohoo',s_id
    return didit()


def terminalUpdate():
    print('Number of active threads:',num_active_threads)
    print('Thread status:',thread_status_dict)


def get_session_ids():
    return get_int_dirnames(ROOT)

def constructData():

    global num_active_threads
    num_active_threads = 0

    session_ids = get_session_ids()

    if session_ids is None:
        print "Failed to get session data"
        return None

    wipe_working_tags(session_ids)

    def session_needs_worker(s_id):
        return not os.path.isfile('%s%d/working'%(ROOT, s_id)) and not os.path.isfile('%s%d/done'%(ROOT, s_id))

    for s_id in session_ids:

        if not session_needs_worker(s_id):
            print s_id,'already processed'
            continue
        while num_active_threads >= MAX_ACTIVE_THREADS:
        #    terminalUpdate()
            pass

        change_num_active_threads(1)

        thread.start_new_thread( worker, (s_id,) )
        terminalUpdate()

    print 'end '
    while 1:
        # leave terminal open for threads to output to
        pass
