#!/usr/bin/env python
import os
import re
from collections import defaultdict
from datetime import datetime
from itertools import islice

from iribaker import to_iri
from rdflib import URIRef, Literal

import constants as c
import load_json as h


global meps
global dossiers
global parties

def init_globals():

    def init_meps():
        global meps
        if os.path.isfile(c.DICT_MEPS): meps = h.load_json(c.DICT_MEPS)
        else: raise Exception('MEPs data file not found.')

    def init_parties():
        global parties
        if os.path.isfile(c.DICT_PARTIES): parties = h.load_json(c.DICT_PARTIES)
        else: raise Exception('Parties data file not found')

    def init_dossiers():
        global dossiers
        dossiers = defaultdict(list)

    init_meps()
    init_parties()
    init_dossiers()


# Needs changing?
def id_to_iri(id_):
    return URIRef(to_iri(c.ont + str(id_)))


def format_name_string(input_string):
    input_string = re.sub('\(.+?\)', '', input_string)
    input_string = input_string.lower().title().encode('utf-8').strip()
    input_string = re.sub('\s+', '_', input_string)
    return input_string


def name_to_dbr(name):
    formatted = format_name_string(name)
    iri = to_iri(c.dbr + formatted)
    #uriref = URIRef(iri)
    return iri

# TODO: See if there is a better dossier url to use instead of dossier['meta']['source']
# TODO: See if there is a better dossier text to use instead of dossier['procedure']['title']
def convert_dossier(path, dataset, graph):

    dossier_data = h.load_json(path)

    for dossier in islice(dossier_data, 0, c.DOSSIER_LIMIT):
        for activity in dossier['activities']:
            if 'type' in activity and activity['type'] == c.DOSSIER_TYPE:

                dossier_id = dossier['_id']
                dossier_url = Literal(dossier['meta']['source'], datatype=c.URI)
                dossier_date = Literal(datetime.strptime(dossier['activities'][0]['date'].split('T')[0], '%Y-%m-%d').date(),datatype=c.DATE)
                dossier_title = Literal(dossier['procedure']['title'].strip(), datatype=c.STRING)

                # Use the meta url as the iri
                dossier_uri = URIRef(to_iri(dossier_url))

                graph.add((dossier_uri, c.PROCESSED_BY, c.EUROPEAN_PARLIAMENT))
                # graph.add((dossier_uri, RDF.type, DOSSIER))
                dataset.add((dossier_uri, c.DOSSIER_TITLE, dossier_title))
                dataset.add((dossier_uri, c.URI, dossier_url))
                dataset.add((dossier_uri, c.DATE, dossier_date))

                # Store the id and uri in the dictionary for use later
                dossiers[dossier_id].append(dossier_uri)

                # dossier matches DOSSIER_TYPE, no need to search more activities
                break

    print
    return dataset, graph


def convert_votes(path, dataset, graph):

    json_data = h.load_json(path)

    m = {'Abstain':c.ABSTAINS,'For':c.VOTES_FOR,'Against':c.VOTES_AGAINST}

    for votes in islice(json_data, 0, c.VOTES_LIMIT):

        if 'dossierid' in votes:

            dossier_id = votes['dossierid']

            # If this dossier is in our dictionary of useful dossiers, continue
            if dossier_id in dossiers:
                dossier_uri = dossiers[dossier_id][0]
                # title = votes['title']
                # url = dossier['url']
                # ep_title = dossier['eptitle']
                for vote_direction in m:
                    if vote_direction in votes:
                        for group in votes[vote_direction]['groups']:
                            # group_name = group['group']
                            for vote in group['votes']:
                                # user_id = vote['userid']
                                voter_id = str(vote['ep_id'])
                                if voter_id in meps:
                                    graph.add((URIRef(meps[voter_id][0]), m[vote_direction], dossier_uri))

                print 'Votes on dossier:', dossier_uri
    print
    return dataset, graph


def convert_mep(path, dataset, graph):
    json_data = h.load_json(path)

    for mep in islice(json_data, 0, c.MEP_LIMIT):
        # Get raw values
        user_id = str(mep['UserID'])
        full_name = Literal(mep['Name']['full'].lower().title().encode('utf-8').strip(), datatype=c.STRING)
        profile_url = Literal(mep['meta']['url'], datatype=c.URI)
        mep_uri = name_to_dbr(full_name)

        # append to global dictionary
        if not meps[user_id]:
            meps[user_id].append(mep_uri)
        mep_uri = URIRef(mep_uri)

        if 'Photo' in mep:
            photo_url = Literal(mep['Photo'], datatype=c.THUMBNAIL)
            dataset.add((mep_uri, c.URI, photo_url))

        if 'Birth' in mep:
            if 'date' in mep['Birth']:
                birth_date = mep['Birth']['date']
                if birth_date != '':
                    birth_date = Literal(datetime.strptime(birth_date.split('T')[0], '%Y-%m-%d').date(),
                                         datatype=c.DATE)
                    dataset.add((mep_uri, c.BIRTH_DATE, birth_date))

            if 'place' in mep['Birth']:
                birth_place = mep['Birth']['place'].strip()
                dataset.add((mep_uri, c.BIRTH_PLACE, URIRef(name_to_dbr(birth_place))))

        if 'Death' in mep:
            death_date = mep['Death']
            death_date = Literal(datetime.strptime(death_date.split('T')[0], '%Y-%m-%d').date(), datatype=c.DATE)
            dataset.add((mep_uri, c.DEATH_DATE, death_date))

        # if 'active' in mep: active = mep['active'] # interesting but unused atm

        # twitter = mep['Twitter']

        # Can be expanded to process all groups. For now takes the latest known
        if 'Groups' in mep:
            # For different memberships
            # if organisationRole = mep['Groups'][0]['role'] == 'member':
            # memberOf
            # if organisationRole = mep['Groups'][0]['role'] == 'xxx':
            # xxx
            # elif organisationRole = mep['Groups'][0]['role'] == 'xxx':
            # xxx

            party_title = mep['Groups'][0]['Organization']
            party_dbr = name_to_dbr(party_title)

            party_id = mep['Groups'][0]['groupid']
            if type(party_id) is list:
                for pid in party_id:
                    if party_dbr not in parties[pid]:
                        parties[pid].append(party_dbr)
                party_id = party_id[0]
            elif party_dbr not in parties[party_id]:
                parties[party_id].append(party_dbr)


            party_uri = URIRef(parties[party_id][0])
            # If a valid iri was added manually, it's always first, so just take the first
            #graph.add((mep_uri, c.MEMBER_OF, URIRef(dict_party[party_id][0])))
            dataset.add((mep_uri, c.PARTY, party_uri))
            graph.add((party_uri, c.IN_LEGISLATURE, c.EUROPEAN_PARLIAMENT))

        if 'Gender' in mep:
            gender = mep['Gender']
            if gender == 'M':
                dataset.add((mep_uri, c.GENDER, c.MALE))
            elif gender == 'F':
                dataset.add((mep_uri, c.GENDER, c.FEMALE))

        dataset.add((mep_uri, c.FULL_NAME, full_name))
        dataset.add((mep_uri, c.URI, profile_url))
        dataset.add((mep_uri, c.OFFICE, c.MEMBER_OF_EU))

        print 'MEP:', mep_uri

    print
    return dataset, graph
