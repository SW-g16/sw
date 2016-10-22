import constants as c

def process_votes(votes_data, bill_uri):
    triples = []

    for k in range(0, 3):

        if c.VOTE_KEYS[k] not in votes_data: continue

        for vote in votes_data[c.VOTE_KEYS[k]]:

            if vote is None: continue

            # Sometimes, `vote` is the string "VP" for some reason.
            #  we ignore these for now.
            # Important: if we infer results based on number of votes,
            #  it's very important that we collect all votes
            #  (i.e. don't ignore, like we do here)

            if isinstance(vote, basestring):
                print "huh. (%s)" % vote

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

            triples.append((voter_uri, ':memberOf', party_uri))
            triples.append((voter_uri, ':represents', state_uri))

    return triples