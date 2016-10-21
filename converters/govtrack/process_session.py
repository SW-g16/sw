import requests
import helpers
import constants as c

def process_session(session_id, empty_threshold):

    # this is where most of the adaption to the endpoint happens.
    # this function processes a 'session' - a piece of the totality of congress'
    #   bills and laws, delimited by time.
    # there is currently a total of 114 historic sessions,
    #  and this function processes all the bills and votes for one of them.

    # we declare an array of triples which we will fill while traversing the data directory

    triples = []

    # after ca every 10000 triples, we send our triples to stardog,
    #  before emptying our local triples variable and filling it up again.
    # this is done to avoid a too large memory usage.

    def send_to_db(triples):
        s = '@prefix : <http://www.votes.example.com/> .\n'
        for t in triples: s += "%s %s %s .\n" % t
        #print 'put %d triples in db' %len(triples)
        return requests.post('http://localhost:5000/store',data={'data':s})

    # every session's bills and votes are available within data/congress/<session_id>/votes .
    # the votes folders have a variable number of subfolders, which we call vote_groups.

    vote_groups = helpers.get_int_dirnames('%s%d/votes' % (c.ROOT, session_id))

    # check if vote_groups is ok

    if vote_groups is None: return []

    # cache the number of triples

    num_triples = 0

    # navigate through all the vote_groups.

    for g in vote_groups:

        # get pointers to bill data (yes, contained within the votes/g folder)

        bills = helpers.get_dirnames('%s%d/votes/%d' % (c.ROOT, session_id , g))

        # for all the bills

        for b in bills:


            if len(triples)>empty_threshold:
                send_to_db(triples)
                triples = []

            # if bill reference looks weird, ignore it

            if b[0]!='s' and b[0]!='h': continue

            # get the individual bills' data from a json file

            bill_data = helpers.loadJsonFile('%s%d/votes/%d/%s/data.json' % (c.ROOT, session_id , g, b))

            # if the bill data is no good, ignore it

            if bill_data is None or 'votes' not in bill_data: continue

            # we generate a uri for the bill

            bill_uri = '<gt_b/%d>' % bill_data['number']

            # retrieve the bill text

            bill_text = '"%s"' % bill_data['question'].replace('"', '').replace('\'', '')

            # add the bill and it's text to our graph

            triples.append((bill_uri,':text',bill_text))
            #num_triples+=1

            for k in range(0,3):


                if len(triples)>empty_threshold:
                    send_to_db(triples)
                    triples = []

                if c.VOTE_KEYS[k] not in bill_data['votes']: continue

                for vote in bill_data['votes'][c.VOTE_KEYS[k]]:

                    if vote is None: continue

                    # Sometimes, `vote` is the string "VP" for some reason.
                    #  we ignore these for now.
                    # Important: if we infer results based on number of votes,
                    #  it's very important that we collect all votes
                    #  (i.e. don't ignore, like we do here)

                    if isinstance(vote, basestring):
                        print "huh. (%s)"%vote

                    # We have these Three pieces of information for each vote,
                    #  in addition to the vote direction (yay/nay/abstain)
                    # note: more data on voters is available in govtrack's 'congress-legislators' bulk data directory

                    voter_uri = '<gt_v/%s>' % vote['id']
                    party_uri = '<gt_p/%s>' % vote['party']
                    state_uri = '<gt_s/%s>' % vote['state']

                    # this is always unique information

                    triples.append((voter_uri, c.VOTE_PROPERTIES[k], bill_uri))

                    # the below two lines are repeated many times, because the same voters vote for more than one bill.
                    # however it is unavoidable if want to account for possible change of state or party membership.
                    # fortunately stardog detects and prunes away duplicate triples,
                    #  so we don't need to worry about polluting our database

                    triples.append((voter_uri, ':partyMemberOf', party_uri))
                    triples.append((voter_uri, ':representsState', state_uri))
                    """
                    num_triples+=3

                    if num_triples > empty_threshold:
                        send_to_db(triples)
                        triples = []
                    """
                    # if we have a certain amount of triples already,
                    #   empty them into stardog


    send_to_db(triples)

    return True
