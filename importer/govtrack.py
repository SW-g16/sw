
import urllib2

import time
from flask import json

TEST = True

# number of bills to query per bulk
BULK_SIZE = 100
if TEST:
    BULK_SIZE = 20

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
        return [parseVoteEvent(vote_event), ':bill_text', parseBillText(vote_event)]

    # called numberOfVoteEvents * numberOfVoters times
    def parseVoter(a):
        return '<https://www.govtrack.us/api/v2/person/' + str(a)+">"

    def parseDirection(o):
        return {'+': ':votesYay','-': ':votesNay','0': ':abstains'}[o['key']]

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

    offset = 0
    def parseDate(date):
        return "\"" + date[:10] + "\"^^xsd:date"

    def parseVoteDate(voting_data):
        return [parseVoteEvent(voting_data),'xsd:date',parseDate(voting_data['created'])]

    def parse_votingAssembly(chamber):
        if chamber == "house":
            return "dbr:United_States_House_of_Representatives"
        elif chamber == "senate":
            return "dbr:United_States_Senate"
        else:
            print "not house or senate:",chamber

    start_time = time.time()
    times = []
    i = 0

    voter_dict = {}

    while (offset < num_voteEvents):

        vote_events = get_voteEventBulk()

        for vote_event in vote_events:
            print "Vote Event" , vote_event['id']
            # add the bill text
            bill_text_triples.append(billTextTriple(vote_event))

            # get the individual votesr
            votes = get_votingData(vote_event)
            vote_date_triples.append(parseVoteDate(vote_event))

            votingAssembly = parse_votingAssembly(vote_event['chamber'])

            for vote in votes:

                print "Vote #",vote['id']

                voter_id = vote['person']['id']

                if voter_id not in voter_dict:
                    voter_dict[voter_id] = {
                        'birthdate':vote['person']['birthday'],
                        'party':get_partyMembership(voter_id),
                        'voting_assemblies':[]}

                if votingAssembly not in voter_dict[voter_id]['voting_assemblies']:
                    voter_dict[voter_id]['voting_assemblies'].append(votingAssembly)

                voter_vote_triples.append(voterVotesTriple(vote, vote_event))

                if TEST and False:
                    i+=1
                    if i>5:
                        i=0
                        break

            times.append(time.time() - start_time)
            start_time = time.time()

        offset += BULK_SIZE

        # to be nice to the data provider during testing
        if TEST:
            break

    party_membership_triples = []
    birthday_triples = []
    voting_assembly_triples = []

    for u in voter_dict:
        voter = voter_dict[u]
        voter_uri = parseVoter(u)
        if voter['birthdate'] is not None:
            birthday_triples.append([voter_uri,'dbo:birthDate',parseDate(voter['birthdate'])])
        if voter['party'] is not None:

            party_membership_triples.append([voter_uri,':memberOf','"'+voter['party']+'"'])
        voting_assembly_triples += [[voter_uri,':votesIn',va] for va in voter['voting_assemblies']]


    print 'Times per vote event:',times

    prefixes = [
        ['@prefix','dbr:','<http://dbpedia.org/resource/>'],
        ['@prefix','dbo:','<http://dbpedia.org/ontology/>'],
        ['@prefix','rdfs:','<http://www.w3.org/2000/01/rdf-schema#>']]

    return prefixes + bill_text_triples + voter_vote_triples + party_membership_triples \
           + vote_date_triples + birthday_triples + voting_assembly_triples
