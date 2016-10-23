from pprint import pprint

import requests
import time

import bill_processor, fsinterface, constants as c


# this is where most of the adaption to the endpoint happens.
# this function processes a 'session' - a piece of the totality of congress'
#   bills and laws, delimited by time.
# there is currently a total of 114 historic sessions,
#  and this function processes all the bills and votes for one of them.

def send_to_db(triples):
    rdf = '.\n'.join(["%s %s %s" % (t[0],t[1],t[2]) for t in triples if len(t)==3]) + '.'
    requests.post('http://localhost:5000/store', data={'data': rdf})

def process_session(session_id,threshold=1500):
    # we declare an array of triples which we will fill while traversing the data directory

    def depth_1_folders(): return fsinterface.get_int_dirnames('%s%d/votes' % (c.CONGRESS_PATH, session_id))

    def depth_2_folders(g): return fsinterface.get_dirnames('%s%d/votes/%d' % (c.CONGRESS_PATH, session_id, g))

    triples = []
    t_0=0
    for g in depth_1_folders():
        for b in depth_2_folders(g):
            triples += bill_processor.process_bill(session_id, g, b)
    send_to_db(triples)
    return len(triples)