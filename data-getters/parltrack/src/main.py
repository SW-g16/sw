#!/usr/bin/env python

import json
from datetime import datetime
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
from iribaker import to_iri
import os
from itertools import islice
from collections import defaultdict
import re

DATA_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))+'/data/parltrack/'

DATA_MEP = DATA_DIR+'meps.json'
DATA_VOTES = DATA_DIR+'votes.json'
DATA_DOSSIER = DATA_DIR+'dossiers.json'

# Number of elements to mine
MEP_LIMIT = None
DOSSIER_LIMIT = None
VOTES_LIMIT = None

DATABASE = 'http://localhost:5820/#/databases/votes/'
NAMESPACE = DATABASE

ont = 'http://votes.examples.com/ontology/'
ONT = Namespace(ont)
PREFIX = ''

DOSSIER_TYPE = 'Legislative proposal published'

#eo = 'http://www.w3.org/2003/01/geo/wgs84_pos#'
#GEO = Namespace(geo)

dbo = 'http://dbpedia.org/ontology/'
DBO = Namespace(dbo)
dbr = 'http://dbpedia.org/resource/'
DBR = Namespace(dbr)
dbp = 'http://dbpedia.org/property/'
DBP = Namespace(dbp)

foaf = 'http://xmlns.com/foaf/0.1/'
FOAF = Namespace(foaf)

DOSSIER = ONT['Bill']
DOSSIER_TITLE = ONT['bill_text']
PROCESSED_BY = ONT['processedBy']

ABSTAINS = ONT['abstains']
VOTES_FOR = ONT['votesYay']
VOTES_AGAINST = ONT['votesNay']
VOTES_IN = ONT['votesIn']

MEMBER_OF = ONT['memberOf']
#dul:isMemberOf
#CURRENT_MEMBER_OF
#PAST_MEMBER_OF

GENDER = DBO['gender']
MALE = DBR['Male']
FEMALE = DBR['Female']
EUROPEAN_PARLIAMENT = DBR['European_Parliament']
#http://dbpedia.org/ontology/europeanParliamentGroup

FULL_NAME = FOAF['name']
BIRTH_DATE = DBO['birthDate']
DEATH_DATE = DBO['deathDate']
BIRTH_PLACE = DBO['birthPlace']

URI = XSD['anyURI']
STRING = XSD['string']
DATE = XSD['date']

# maps mep id to dbr iri
dict_mep = defaultdict(list)
dict_dossier = defaultdict(list)

def load_json(path):
    f = open(path, 'r')
    print 'Loading file:', path
    print '(This will take a while)'
    json_data = json.load(f)
    f.close()
    return json_data

#def mepid_to_profile_iri(id):
 #   return URIRef(to_iri('http://www.europarl.europa.eu/meps/en/' + str(id) + '/_history.html'))

# Needs changing?
def id_to_iri(id):
    return URIRef(to_iri(ont + str(id)))

def format_name_string(input_string):
    input_string = re.sub('\(.+?\)','', input_string)
    input_string = input_string.lower().title().encode('utf-8').strip()
    input_string = re.sub('\s+', '_', input_string)
    return input_string

def name_to_dbr(name):
    formatted = format_name_string(name)
    iri = to_iri(dbr + formatted)
    uriref = URIRef(iri)
    return uriref

# TODO: See if there is a better dossier url to use instead of dossier['meta']['source']
# TODO: See if there is a better dossier text to use instead of dossier['procedure']['title']
def convert_dossier(path, dataset, graph_uri):
    json_data = load_json(path)

    graph = dataset.graph(graph_uri)

    for dossier in islice(json_data, 0, DOSSIER_LIMIT):
        for activity in dossier['activities']:
            if 'type' in activity:
                if activity['type'] == DOSSIER_TYPE:
                    dossier_id = dossier['_id']
                    dossier_url = Literal(dossier['meta']['source'], datatype=URI)
                    dossier_date = Literal(datetime.strptime(dossier['activities'][0]['date'].split('T')[0], '%Y-%m-%d').date(), datatype=DATE)
                    dossier_title = Literal(dossier['procedure']['title'].strip(), datatype=STRING)

                    # User the meta url as the iri
                    dossier_uri = URIRef(to_iri(dossier_url))

                    graph.add((dossier_uri, PROCESSED_BY, EUROPEAN_PARLIAMENT))
                    #graph.add((dossier_uri, RDF.type, DOSSIER))
                    dataset.add((dossier_uri, DOSSIER_TITLE, dossier_title))
                    dataset.add((dossier_uri, URI, dossier_url))
                    dataset.add((dossier_uri, DATE, dossier_date))

                    # Store the id and uri in the dictionary for use later
                    dict_dossier[dossier_id].append(dossier_uri)

                    print 'Dossier:', dossier_uri
                    break  # dossier matches DOSSIER_TYPE, no need to search more activities

    return dataset, graph

def convert_votes(path, dataset, graph_uri):
    json_data = load_json(path)

    graph = dataset.graph(graph_uri)

    for votes in islice(json_data, 0, VOTES_LIMIT):
        if 'dossierid' in votes:
            dossier_id = votes['dossierid']

            # If this dossier is in our dictionary of useful dossiers, continue
            if dossier_id in dict_dossier:
                dossier_uri = dict_dossier[dossier_id][0]
                #title = votes['title']
                #url = dossier['url']
                #ep_title = dossier['eptitle']

                if 'Abstain' in votes:
                    for group in votes['Abstain']['groups']:
                        #group_name = group['group']
                        for vote in group['votes']:
                            #user_id = vote['userid']
                            voter_id = vote['ep_id']
                            if voter_id in dict_mep:
                                graph.add((dict_mep[voter_id][0], ABSTAINS, dossier_uri))
                                print 'Abstains dossier:', dossier_uri

                if 'For' in votes:
                    for group in votes['For']['groups']:
                        #group_name = group['group']
                        for vote in group['votes']:
                            #user_id = vote['userid']
                            voter_id = vote['ep_id']
                            if voter_id in dict_mep:
                                graph.add((dict_mep[voter_id][0], VOTES_FOR, dossier_uri))
                                print 'Vote for dossier:', dossier_uri

                if 'Against' in votes:
                    for group in votes['Against']['groups']:
                        #group_name = group['group']
                        for vote in group['votes']:
                            #user_id = vote['userid']
                            voter_id = vote['ep_id']
                            if voter_id in dict_mep:
                                graph.add((dict_mep[voter_id][0], VOTES_AGAINST, dossier_uri))
                                print 'Vote against dossier:', dossier_uri
    return dataset, graph


def convert_mep(path, dataset, graph_uri):
    json_data = load_json(path)

    graph = dataset.graph(graph_uri)

    for mep in islice(json_data, 0, MEP_LIMIT):
        # Get raw values
        user_id = mep['UserID']

        full_name = Literal(mep['Name']['full'].lower().title().encode('utf-8').strip()
, datatype=STRING)

        mep_uri = name_to_dbr(full_name)

        # append to global dictionary
        dict_mep[user_id].append(mep_uri)

        profile_url = Literal(mep['meta']['url'], datatype=URI)

        if 'Photo' in mep:
            photo_url = Literal(mep['Photo'], datatype=URI)
            dataset.add((mep_uri, URI, photo_url))

        if 'Birth' in mep:
            if 'date' in mep['Birth']:
                birth_date = mep['Birth']['date']
                if birth_date != '':
                    birth_date = Literal(datetime.strptime(birth_date.split('T')[0], '%Y-%m-%d').date(), datatype=DATE)
                    dataset.add((mep_uri, BIRTH_DATE, birth_date))

            if 'place' in mep['Birth']:
                birth_place = mep['Birth']['place'].strip()
                dataset.add((mep_uri, BIRTH_PLACE, name_to_dbr(birth_place)))

        if 'Death' in mep:
            death_date = mep['Death']
            death_date = Literal(datetime.strptime(death_date.split('T')[0], '%Y-%m-%d').date(), datatype=DATE)
            dataset.add((mep_uri, DEATH_DATE, death_date))

        if 'active' in mep:
            active = mep['active']

        # twitter = mep['Twitter']

        # Can be expanded to process all groups. For now takes the latest known
        if 'Groups' in mep:
            # For different memberships
            #if organisationRole = mep['Groups'][0]['role'] == 'member':
                # memberOf
            #if organisationRole = mep['Groups'][0]['role'] == 'xxx':
                # xxx
            #elif organisationRole = mep['Groups'][0]['role'] == 'xxx':
                # xxx

            organisation_title = name_to_dbr(mep['Groups'][0]['Organisation'])
            graph.add((mep_uri, MEMBER_OF, organisation_title))

            #organisationId = mep['Groups'][0]['groupid']

        if 'Gender' in mep:
            gender = mep['Gender']
            if gender == 'M':
                dataset.add((mep_uri, GENDER, MALE))
            elif gender == 'F':
                dataset.add((mep_uri, GENDER, FEMALE))

        dataset.add((mep_uri, FULL_NAME, full_name))
        dataset.add((mep_uri, URI, profile_url))

        #graph.add((mep_uri, MEMBER_OF, URIRef(to_iri(dbr + 'European_Parliament'))))

        print 'MEP:', mep_uri

    return dataset, graph

def save_dataset(filename, dataset):
    with open(filename, 'w') as f:
        print 'Saving:', filename
        dataset.serialize(f, format='trig')
    print 'Saved.'

dataset = Dataset()
dataset.bind(PREFIX, ONT)
dataset.bind('dbo', DBO)
dataset.bind('dbr', DBR)
dataset.bind('dbp', DBP)
dataset.bind('foaf', FOAF)

dataset, mep_graph = convert_mep(DATA_MEP, dataset, ONT)

dataset, dossier_graph = convert_dossier(DATA_DOSSIER, dataset, ONT)

dataset, votes_graph = convert_votes(DATA_VOTES, dataset, ONT)

save_dataset(DATA_DIR + 'parltrack.trig', dataset)