"""
# here we get data from govtacks' congress-legislators-(current|historic).csv files.
# the files do not overlap - no voters appear in both files

# these are the column names, equal for both files

    last_name	first_name	birthday	gender	type	state	district	party
    url	address	phone	contact_form	rss_url	twitter	facebook	facebook_id
    youtube	youtube_id	bioguide_id	thomas_id	opensecrets_id	lis_id	cspan_id
    govtrack_id	votesmart_id	ballotpedia_id	washington_post_id	icpsr_id	wikipedia_id

# we're interested in these

0   last name
1   first name
2   birthday
3   gender
4   type // senator or house representative
5   state acronym
7   party
18  bioguide_id // necessary because this identifier is used in voting data
23  govtrack_id // necessary because this is the best choice for uri (can be used to visit voter object govtrack http endpoint)
28  wikipedia_id // having a wikipedia article indicates significance / public awareness of the individual, which is an interesting measure

# this is how we format our triples to store each of the things

0   foaf:firstname
1   foaf:lastname
// 2 // todo birthday
3   foaf:gender
4   :votesIn dbr:United_States_House_of_Representatives | :votesIn dbr:United_States_Senate
5   :respresentsState dbr:Mississippi // however we get only the acronym. we use the map ross linked to to get the whole name
7   :memberOf dbr:Republican_Party_(United_States)
18  :sameAs <uri_generated_by_votes_getter/bioguide_id>  // <-- indicate equality with already stored voter
23  :<http://www.govtrack.us/api/v2/person/govtrack_id>  // <-- the main uri for our voter
28  :wikipedia <http://www.wikipedia.org/wiki/wikipedia_id>

"""
import csv
import os
import time

import send_to_db

states = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona',
          'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware',
          'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois',
          'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland',
          'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MP': 'Northern Mariana Islands',
          'MS': 'Mississippi', 'MT': 'Montana', 'NA': 'National', 'NC': 'North Carolina', 'ND': 'North Dakota',
          'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada',
          'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico',
          'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas',
          'UT': 'Utah', 'VA': 'Virginia', 'VI': 'Virgin Islands', 'VT': 'Vermont', 'WA': 'Washington',
          'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'}

fail_states = []


def make_safe(string):
    return ''.join(e for e in string if e.isalnum() or e == ' ')


def represents_triple(voter_uri, state_acronym, i, path):
    # some state acronyms be bad
    try:
        return voter_uri, ':represents', 'dbr:' + states[state_acronym].replace(' ', '_')
    except:
        fail_states.append((state_acronym, i, path[len(path) - 12:]))
        return None


def get_voter_uri(param):
    if param == '' or param is None: return None
    return '<http://www.govtrack.us/api/v2/person/%s>' % param


party_uri_map = {
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
    # jesus fucking christ
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

"""
'Conservative':'dbr:',
'Ind. Democrat':'dbr:',
'Law and Order':'dbr:',
'Liberty':'dbr:',
'Free Soil':'dbr:',
'Ind. Republican-Democrat':'dbr:',
'Ind. Whig':'dbr:',
'Unionist':'dbr:',
'States Rights':'dbr:',
'Anti-Lecompton Democrat':'dbr:',
'Constitutional Unionist':'dbr:',
'Independent Democrat':'dbr:',
'Unconditional Unionist':'dbr:',
'Conservative Republican':'dbr:',
'Ind. Republican':'dbr:',
'Liberal Republican':'dbr:',
'National Greenbacker':'dbr:',
'Readjuster Democrat':'dbr:',
'Readjuster':'dbr:',
'Union':'dbr:',
'Union Labor':'dbr:',
'Populist':'dbr:',
'Silver Republican':'dbr:',
'Free Silver':'dbr:',
'Democratic and Union Labor':'dbr:',
'Progressive Republican':'dbr:',
'Progressive':'dbr:',
'Prohibitionist':'dbr:',
'Socialist':'dbr:',
'Farmer-Labor':'dbr:',
'Nonpartisan':'dbr:',
'Coalitionist':'dbr:',
'Popular Democrat':'dbr:',
'American Labor':'dbr:',
'New Progressive':'dbr:',
'Republican-Conservative':'dbr:',
'Democrat-Liberal':'dbr:'

"""


def get_party(key):
    if key in party_uri_map:
        return party_uri_map[key]
    else:
        return '"%s"' % key


def gender_triple(voter_uri, gender_key):
    if gender_key == 'M':
        k = '"male"'
    elif gender_key == 'F':
        k = '"female"'
    else:
        return None
    return voter_uri, 'foaf:gender', k


def votes_in_triple(voter_uri, voting_assembly_key):
    if voting_assembly_key == 'rep':
        va_uri = 'dbr:United_States_House_of_Representatives'
    elif voting_assembly_key == 'sen':
        va_uri = 'dbr:United_States_Senate'
    else:
        return None
    return voter_uri, ':votesIn', va_uri


def parse_row(row, i, path):
    # voter uri, using govtrack id.
    # advantage: can be used to access govtrack voter obects,
    #   like https://www.govtrack.us/api/v2/person/411931
    voter_uri = get_voter_uri(row[23])
    if voter_uri is None: return []

    possibles = [
        gender_triple(voter_uri, row[3]),
        votes_in_triple(voter_uri, row[4]),
        represents_triple(voter_uri, row[5], i, path)
    ]

    return [
               (voter_uri, 'foaf:lastName', '"%s"' % make_safe(row[0])),
               (voter_uri, 'foaf:firstName', '"%s"' % make_safe(row[1])),
               (voter_uri, ':memberOf', "%s" % get_party(row[7])),
               (voter_uri, 'owl:sameAs', '<http://api.stardog.com/gt_v/%s>' % row[18]),
               (voter_uri, ':wikipedia', '<http://www.wikipedia.org/wiki/%s>' % row[28].replace(' ', '_'))
           ] + [p for p in possibles if p is not None]


def get_paths():
    file_suffixes = ['current.csv', 'historic.csv']
    root = os.path.dirname(os.path.realpath(__file__)) + '/../../../data/govtrack/congress-legislators/legislators-'
    return [root + s for s in file_suffixes]


def process_voters():
    start = time.time()
    paths = get_paths()

    triples = [('@prefix', ':', '<http://votes.example.com/ontology/>'),
               ('@prefix', 'dbr:', '<http://dbpedia.org/resource/>'),
               ('@prefix', 'owl:', '<http://www.w3.org/2002/07/owl#>'),
               ('@prefix', 'foaf:', '<http://xmlns.com/foaf/0.1/>')]

    for path in paths:
        with open(path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            next(reader)  # ignore headers
            for i, row in enumerate(reader): triples += parse_row(row, i, path)

    # print 'Got these bad state acronyms: (acronym, row number, file):', fail_states
    duration = time.time()-start
    print 'Processed voters. Stardog response: %s. %d triples stored in %0.2f seconds. %0.2f triples per seconds.' % ( send_to_db.send_to_db(triples), len(triples), duration, len(triples) / duration)
