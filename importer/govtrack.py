
import urllib2

from flask import json

BULK_SIZE = 10 # number of bills to query per bulk
GT_PREFIX = "https://www.govtrack.us/api/v2/"

def constructData():
    
    def parseDirection(o):

        if o['value'] == "Yea" or o['key'] == "+":
            return "v:votesYay"
        elif o['value'] == "Nay" or o['key'] == "-":
            return "v:votesNay"
        elif o['value'] == "Not Voting" or o['key'] == '0':
            return "v:abstain"

    def parseVoter(a):
        return '<' + GT_PREFIX + 'person/' + str(a) + '>'

    r = urllib2.urlopen(GT_PREFIX+"vote?limit=0").read()
    number_of_vote_events = json.loads(r)['meta']['total_count']

    print "GovTrack has ", number_of_vote_events , " voting events. "
    print "We get their related data in bulks of ", BULK_SIZE , ' voting events.'
    print "During testing we limit to 1 bulk. "

    offset = 0

    triples = []

    while (offset<number_of_vote_events):

        r = urllib2.urlopen(GT_PREFIX+"vote?offset="+str(offset)+"&limit="+str(BULK_SIZE)).read()
        vote_events = json.loads(r)['objects']

        triples = []

        for i in vote_events:

            print i['id']

            text = i['question']
            bill_uri = '<'+GT_PREFIX + 'vote?id='+str(i['id'])+'>'
            triples.append([bill_uri,'v:text',"\""+text.replace('"','').replace('\'','')+"\""])

            voting_data = json.loads(urllib2.urlopen(GT_PREFIX+"vote_voter?vote="+str(i['id'])).read())['objects']

            for vote in voting_data:
                voter_uri = parseVoter(vote['person']['id'])
                direction = parseDirection(vote['option'])
                triples.append([voter_uri,direction,bill_uri])

        offset += BULK_SIZE
        break


    return triples