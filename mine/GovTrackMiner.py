# coding: utf-8
import json
import requests
import datetime
import time
from multiprocessing.pool import ThreadPool

from Miner import Miner

SENATE = 'dbr:United_States_Senate'
HOUSE = 'dbr:United_States_House_of_Representatives'


# mapping of strings found in the 'party' field of voters, onto dbpedia entries (or wikipedia, when no dbpedia available/found)
PARTY_URI_MAP = {
    'Democrat': 'dbr:Democratic_Party_\(United_States\)',
    'Republican': 'dbr:Republican_Party_\(United_States\)',
    'Independent': 'dbr:Independent_politician',
    'Anti-Administration': 'dbr:Anti-Administration_Party',
    'Pro-Administration': 'dbr:Pro-Administration_Party',
    'Federalist': 'dbr:Federalist_Party',
    'American': 'dbr:Know_Nothing',
    'Whig': 'dbr:Whig_Party_\(United_States\)',
    'Adams': 'dbr:National_Republican_Party',
    'Adams Democrat': 'dbr:National_Republican_Party',
    'Anti-Jacksonian': 'dbr:National_Republican_Party',
    'Anti-Jackson': 'dbr:National_Republican_Party',
    'Anti Jacksonian': 'dbr:National_Republican_Party',
    'Anti Jackson': 'dbr:National_Republican_Party',
    'Democratic-Republican': 'dbr:Democratic-Republican_Party',
    'Jakson': 'dbr:Democratic-Republican_Party',
    'Jackson Republican': 'dbr:Democratic-Republican_Party',
    'Crawford Republican': 'dbr:Democratic-Republican_Party',
    'Jacksonian': 'dbr:Democratic-Republican_Party',
    'Nullifier': '<https://en.wikipedia.org/wiki/Nullifier_Party>',
    'Anti Masonic': 'dbr:Anti-Masonic_Party',
    'Union Democrat': '<https://en.wikipedia.org/wiki/Union_Democratic_Party>'
}



class GovTrackMiner(Miner):

    URL_API = 'https://www.govtrack.us/api/v2/'
    URL_BILL = '%sbill' % URL_API
    URL_PERSON = '%sperson' % URL_API
    URL_VOTE = '%svote' % URL_API
    URL_VOTERVOTE = '%svote_voter' % URL_API


    def __init__(self, db, namespaces, test):
        super(GovTrackMiner, self).__init__(db, namespaces, test)
        self.since = datetime.datetime.fromtimestamp(int((time.time()-test*24*60*60))).strftime('%Y-%m-%d') if test else '1750-01-01'
        if test:
            print 'Inited govtrack miner, will mine for the past %s days (since %s)' % (test, self.since)

    def fetch(self,url):
        response = requests.get(url,timeout=10)
        if response.status_code==200: return json.loads(response.text)
        else: print 'fail %s' % url

    def mine(self):

        # todo do some testing to find a good value for how many triples to keep in `trips` before unloading into db

        # an alternative approach to the extraction of certain kinds of data that's done here, is to convert all
        # the api's returned json objects into triples, without looking much at them, could generate uris on the fly.
        # this would give more data but we'd understand it less

        r=ThreadPool(3).map(lambda x:x(), [self.__mine_individual_votes__,self.__mine__persons__,self.__mine__bills__])
        print 'Govtrack done with mining'
        return r


    def __mine__persons__(self):
        # can't sort by 'since', get limited amount of data from vote_voter instead
        # could get list of api urls from db, and look up one by one in the api
        # but what more is interesting, when we already know how they vote?
        pass
        return True

    timeformat = lambda _, t : '"%s"^^xsd:date' % t.split('T')[0] #'"%s"' % strptime(t.split('T')[0], '%Y-%m-%d')



    def __mine__bills__(self):

        since = self.since
        limit = 6000 # max

        while True:

            # don't need number of votes for/against/abstain/present, can infer after mine_individual_votes
            url = '%s?created__gt=%s&limit=%s&fields=category_label,chamber_label,congress,session,result,created,question,required,link' % (self.URL_VOTE, since, limit)
            try:
                vote_json = self.fetch(url)
            except:
                # data unavailable, corrupted, or connection is down or slow
                # could be either temporary or permanent problem
                # todo implement retrying a few times before giving up on this url
                continue
            objects = vote_json['objects']
            assert isinstance(objects,list), objects

            if len(objects) == 0:
                # reached most recent object
                break

            since = vote_json['objects'][-1]['created']

            for obj in objects:
                subject = '<%s>' % obj['link']

                if 'category_label' in obj: self.add_triple('%s votes:votable_category "%s".' % (subject, obj['category_label'].lower()))

                self.add_triple('%s votes:session %s.' % (subject, obj['session']))
                self.add_triple('%s votes:congress %s.' % (subject, obj['congress']))
                self.add_triple('%s votes:voting_time %s.' % (subject, self.timeformat(obj['created']))) #  todo verify 'created' is actually the voting time
                self.add_triple('%s votes:result_text "%s".' % (subject, obj['result'].replace('"','\''))) # todo better string cleaning
                self.add_triple('%s votes:bill_text "%s".' % (subject, obj['question'].replace('"','\'')))
                try:
                    self.add_triple('%s votes:required_upvote_proportion "%s"^^xsd:float.' % (subject, round(float(obj['required'].split('/')[0])/float(obj['required'].split('/')[1]),2)))
                except:
                    # found a 'QUOROM' value
                    # not sure what it means. skipping for now
                    pass
                # there's room for a lot more extraction of data and refining of the ontology.
                # there's https://www.govtrack.us/api/v2/bill, but this is left untouched
                # bills are complicated things that pass through different chambers and whatnot,
                # they're part of processes and are of different kinds
                # todo study law/political science, then refine ontology

        self.add_to_db(self.triples)
        print 'Govtrack done mining representatives'
        return True

    def __mine_individual_votes__(self):

        since = self.since
        limit = 6000 # max

        while True:

            votervote_url = '%s?created__gt=%s&limit=%s&fields=created,option__key,option__vote,person_role__person,person__link,person__name,person__birthday,person__gender,person_role__party,vote__link' % (self.URL_VOTERVOTE,since,limit)

            votervote_json = self.fetch(votervote_url)
            objects = votervote_json['objects']
            assert isinstance(objects,list), objects

            if len(objects) == 0:
                # reached most recent object
                break

            since = votervote_json['objects'][-1]['created']


            for obj in objects:

                # todo clean strings more properly, should be robust

                direction = obj['option']['key']

                if direction=='P': voteverb = '%s:present' % self.namespaces.VOTES
                elif direction=='+': voteverb = '%s:upvotes' % self.namespaces.VOTES
                elif direction=='-': voteverb = '%s:downvotes' % self.namespaces.VOTES
                elif direction=='0': voteverb = '%s:abstains' % self.namespaces.VOTES
                else: raise Exception('unexpected vote verb : %s' % direction)

                vote = obj['option']['vote']
                voter = obj['person_role']['person']
                assert isinstance(vote, int), 'Unexpected voter id %s' % voter
                assert isinstance(vote, int), 'Unexpected vote id %s' % vote

                votable_api_url = '<%s/%s>' % (self.URL_VOTE,vote)
                voter_api_url = '<%s/%s>' % (self.URL_PERSON, voter)


                # the most central kind of voting data: voter votesfor something
                self.add_triple('%s %s %s.' % (voter_api_url,voteverb, votable_api_url))

                # strangely, the unique id for api reference is only available in /vote_voter.
                # example: the unique identifier 13966 is not available at https://www.govtrack.us/api/v2/vote/13966
                # the api url is useful for accessing more data later, but we need the non-api unique url
                # to be able to recognize this votable later
                # so we link it with owl:sameAs
                votable_nonapi_url = '<%s>' % obj['vote']['link']
                self.add_triple('%s owl:sameAs %s.' % (votable_api_url,votable_nonapi_url))

                # same with /person
                voter_nonapi_url = '<%s>' % obj['person']['link']
                self.add_triple('%s owl:sameAs %s.' % (voter_api_url,voter_nonapi_url))

                # since we can't sort persons by 'since' as we can with /vote_voter and /vote,
                # we get the relevant info from here instead
                # todo figure what bioguideid, cspanid, pvsid, osid are and whether they're useful
                self.add_triple('%s foaf:birthday "%s".' % (voter_api_url,obj['person']['birthday'].encode('utf-8')))
                self.add_triple('%s foaf:gender "%s".' % (voter_api_url,obj['person']['gender'].encode('utf-8')))
                self.add_triple('%s foaf:name "%s".' % (voter_api_url,obj['person']['name'].encode('utf-8')))

                # see comment on this in party-issue.md
                self.add_triple('%s dbo:party %s.' % (voter_api_url, PARTY_URI_MAP[obj['person_role']['party']]))

        self.add_to_db(self.triples)
        print 'Govtrack done mining votes'
        return True

