import time

import constants as c
import helpers
import p_bill
import send_to_db


# this function processes a 'session' - a piece of the totality of congress' bills and laws, delimited by time.
# there is currently a total of 114 historic sessions.
# this function processes all the bills and votes for one of them.

def process_session(session_id):
    start = time.time()

    def depth_1_folders():
        return helpers.get_dirnames('%s%d/votes' % (c.CONGRESS_PATH, session_id))

    def depth_2_folders(k):
        return helpers.get_dirnames('%s%d/votes/%s' % (c.CONGRESS_PATH, session_id, str(k)))

    triples = [('@prefix', ':', '<http://votes.example.com/ontology/>'),
               ('@prefix', 'dbr:', '<http://dbpedia.org/resource/>')]

    for g in depth_1_folders():
        for b in depth_2_folders(g):
            triples += p_bill.process_bill(session_id, g, b)

    processing_time = time.time() - start

    start = time.time()

    send_to_db.send_to_db(triples)

    stardog_time = time.time() - start

    return {'num_triples': len(triples), 'processing_time': processing_time, 'stardog_wait_time': stardog_time}
