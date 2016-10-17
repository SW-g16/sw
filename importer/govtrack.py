
import urllib2

from flask import json

TEST = True

# number of bills to query per bulk
BULK_SIZE = 100
if TEST:
    BULK_SIZE = 3

def constructData():
    
    def get_data(url):
        # we get and parse json-encoded data returned by govtrack.
        return json.loads(urllib2.urlopen(url).read())

    # called once
    def get_numberOfVoteEvents():
        return get_data("https://www.govtrack.us/api/v2/vote?limit=0")['meta']['total_count']

    def helloUser(num_voteEvents):
        print "GovTrack has ", num_voteEvents, " voting events. "
        print "We get their related data in bulks of ", BULK_SIZE, ' voting events.'
        print "During testing we limit to 1 bulk. "

    # called numberOfVoters times
    def get_partyMembership(voter_id):
        return get_data('https://www.govtrack.us/api/v2/person/' + str(voter_id))['roles'][0]['party']

    # called numberOfVoteEvents / BULK_SIZE times
    def get_voteEventBulk():
        return get_data("https://www.govtrack.us/api/v2/vote?offset=" + str(offset) + "&limit=" + str(BULK_SIZE))['objects']

    # called numberOfVoteEvents times
    def get_votingData(vote_event):
        return get_data("https://www.govtrack.us/api/v2/vote_voter?vote=" + str(vote_event['id']))['objects']

    def parseVoteEvent(vote_event):
        return '<https://www.govtrack.us/api/v2/vote?id=' + str(vote_event['id'])+">"

    def cleanString(str):
        return str.replace('"', '').replace('\'', '')

    def parseBillText(vote_event):
        return "\"" + cleanString(vote_event['question']) + "\""

    def billTextTriple(vote_event):
        return [parseVoteEvent(vote_event), 'v:text', parseBillText(vote_event)]

    # called numberOfVoteEvents * numberOfVoters times
    def parseVoter(a):
        return '<https://www.govtrack.us/api/v2/person/' + str(a)+">"

    def parseDirection(o):
        return {'+': 'v:votesYay','-': 'v:votesNay','0': 'v:abstains'}[o['key']]

    def voterVotesTriple(vote,vote_event):
        return [parseVoter(vote['person']['id']), parseDirection(vote['option']), parseVoteEvent(vote_event)]



    num_voteEvents = get_numberOfVoteEvents()

    helloUser(num_voteEvents)


    bill_text_triples = []
    voter_vote_triples = []
    party_membership_dict = {}

    offset = 0

    while (offset < num_voteEvents):

        vote_events = get_voteEventBulk()

        for vote_event in vote_events:
            print vote_event['id']
            # add the bill text
            bill_text_triples.append(billTextTriple(vote_event))

            # get the individual votes
            voting_data = get_votingData(vote_event)

            for vote in voting_data:
                if vote['person']['id'] not in party_membership_dict:
                    party_membership_dict[vote['person']['id']] = get_partyMembership(vote['person']['id'])
                    print party_membership_dict[vote['person']['id']]
                print 'vote ',vote['id']
                voter_vote_triples.append(voterVotesTriple(vote, vote_event))
            break
        offset += BULK_SIZE

        # to be nice to the data provider during testing
        if TEST:
            break

    party_membership_triples = []
    for k in party_membership_dict:
        if party_membership_dict[k] is not None:
            party_membership_triples.append([parseVoter(k),'v:memberOf','"'+party_membership_dict[k]+'"'])
    print party_membership_triples
    return bill_text_triples + voter_vote_triples + party_membership_triples
