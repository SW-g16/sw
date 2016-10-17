
import urllib2

import time
from flask import json

TEST = True

# number of bills to query per bulk
BULK_SIZE = 100
if TEST:
    BULK_SIZE = 5

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
        return '<https://www.govtrack.us/api/v2/vote/' + str(vote_event['id'])+">"

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
        return [
            parseVoter(vote['person']['id']),
                parseDirection(vote['option']),
                parseVoteEvent(vote_event)]


    num_voteEvents = get_numberOfVoteEvents()

    helloUser(num_voteEvents)


    bill_text_triples = []
    vote_date_triples = []
    voter_vote_triples = []
    
    birthday_dict = {}
    party_membership_dict = {}
    

    # instead of voter age, we should get birthdays, and deduce age for each VotingEvent
    #   (as age is different for different VotingEvents).
    # because this is more complicated, we leave it out for now and do this instead,
    #   in order to meet the assignment requirements.
    voter_age_dict = {}

    offset = 0
    def parseDate(date):
        return "\"" + date[:10] + "\"^^xsd:date"

    def parseVoteDate(voting_data):
        return [parseVoteEvent(voting_data),'rdfs:date',parseDate(voting_data['created'])]

    start_time = time.time()
    times = []
    i = 0
    while (offset < num_voteEvents):

        vote_events = get_voteEventBulk()

        for vote_event in vote_events:
            print "Vote Event" , vote_event['id']
            # add the bill text
            bill_text_triples.append(billTextTriple(vote_event))

            # get the individual votesr
            votes = get_votingData(vote_event)
            vote_date_triples.append(parseVoteDate(vote_event))

            for vote in votes:
                print "Vote #",vote['id']
                voter_id = vote['person']['id']
                if voter_id not in birthday_dict:
                    birthday_dict[voter_id] = vote['person']['birthday']
                if voter_id not in party_membership_dict:
                    party_membership_dict[voter_id] = get_partyMembership(voter_id)
                voter_vote_triples.append(voterVotesTriple(vote, vote_event))
                if TEST:
                    i+=1
                    if i>5:break

            times.append(time.time() - start_time)

        offset += BULK_SIZE

        # to be nice to the data provider during testing
        if TEST:
            break

    party_membership_triples = [[parseVoter(k),'v:memberOf','"'+party_membership_dict[k]+'"'] for k in party_membership_dict if party_membership_dict[k] is not None]
    print birthday_dict
    #birthday_triples = [dateTriple(parseVoter(k),'foaf:birthday',birthday_dict[k]) for k in birthday_dict]
    birthday_triples = []
    for i in birthday_dict: birthday_triples.append([parseVoter(k),'dbo:birthDate',parseDate(birthday_dict[k])])

    print 'Times per vote event:',times

    return [['@prefix','dbo:','<http://dbpedia.org/ontology/>'],['@prefix','rdfs:','<http://www.w3.org/2000/01/rdf-schema#>']] + bill_text_triples + voter_vote_triples + party_membership_triples + vote_date_triples + birthday_triples
