
import requests

import bill_processor, fsinterface, constants as c


# this is where most of the adaption to the endpoint happens.
# this function processes a 'session' - a piece of the totality of congress'
#   bills and laws, delimited by time.
# there is currently a total of 114 historic sessions,
#  and this function processes all the bills and votes for one of them.

def process_session(session_id, empty_threshold):
    # we declare an array of triples which we will fill while traversing the data directory

    triples = []

    # after ca every 10000 triples, we send our triples to stardog,
    #  before emptying our local triples variable and filling it up again.
    # this is done to avoid a too large memory usage.

    def send_to_db(triples):
        print'senting to db'
        s = ''
        for t in triples: s += "%s %s %s .\n" % t
        # print 'put %d triples in db' %len(triples)
        r = requests.post('http://localhost:5000/store', data={'data': s})
        print 'back'
        return r

    # every session's bills and votes are available within data/congress/<session_id>/votes .
    # the votes folders have a variable number of subfolders, which we call vote_groups.

    vote_groups = fsinterface.get_int_dirnames('%s%d/votes' % (c.CONGRESS_PATH, session_id))

    # check if vote_groups is ok

    if vote_groups is None: return []

    # navigate through all the vote_groups.

    for g in vote_groups:

        # get pointers to bill data (yes, contained within the votes/g folder)

        bills = fsinterface.get_dirnames('%s%d/votes/%d' % (c.CONGRESS_PATH, session_id, g))

        # for all the bills

        for b in bills:

            triples += bill_processor.process_bill(session_id, g, b)
            print b
            # when we have enough triples, empty them into stardog
            if len(triples) > empty_threshold:
                send_to_db(triples)
                triples = []

    send_to_db(triples)

    return True
