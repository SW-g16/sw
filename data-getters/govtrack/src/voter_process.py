
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
from pprint import pprint

import send_to_db
import os

path = os.path.dirname(os.path.realpath(__file__))+'/../../../data/govtrack/congress-legislators/legislators-current.csv'

import csv

states = {'AK': 'Alaska','AL': 'Alabama','AR': 'Arkansas','AS': 'American Samoa','AZ': 'Arizona','CA': 'California','CO': 'Colorado','CT': 'Connecticut','DC': 'District of Columbia','DE': 'Delaware','FL': 'Florida','GA': 'Georgia','GU': 'Guam','HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}

interesting_indices = [0,1,2,4,5,7,18,23,28]

def get_voter_uri(param):
    return '<http://www.govtrack.us/api/v2/person/%s>'% param

def get_party(key):
    # todo parse properly and return dbpedia uri
    return '"%s"'%key

with open(path, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    headers = []
    i=0

    triples = [
        ('@prefix',':','<http://www.votes.example.com/ontology/>'),
        ('@prefix','dbr:','<http://dbpedia.org/resource/>'),
        ('@prefix','owl:','<http://www.w3.org/2002/07/owl#>'),
        ('@prefix','foaf:','<http://xmlns.com/foaf/0.1/>')
    ]

    for row in spamreader:
        if i==0:
            headers = row
            i=1
            pprint(headers)
            continue

        pprint(row)



        # voter uri, using govtrack id.
        # advantage: can be used to access govtrack voter obects,
        #   like https://www.govtrack.us/api/v2/person/411931
        voter_uri = get_voter_uri(row[23])

        first_name_triple = (voter_uri, 'foaf:firstName', '"%s"'% row[0])

        last_name_triple = (voter_uri,'foaf:lastName','"%s"'%row[1])

        gender_triple = (voter_uri,'foaf:gender','"male"' if row[2]=='M' else '"female"')

        votesIn_triple = (voter_uri,':votesIn','dbr:United_States_House_of_Representatives' if row[4] == 'rep' else 'dbr:United_States_Senate')

        representsState_triple = (voter_uri,':representsState','dbr:'+states[row[5]].replace(' ','_'))

        party_triple = (voter_uri,':memberOf' , "%s" % get_party(row[7]))

        bioguide_id_triple = (voter_uri,'owl:sameAs','<gt_v/%s>'%row[18]) # associate with reviously stored voters

        wikipedia_id_triple = (voter_uri,':wikipedia','<http://www.wikipedia.org/wiki/%s>'%row[28])

        triples += [first_name_triple, last_name_triple, gender_triple,votesIn_triple,representsState_triple, party_triple
#bioguide_id_triple,wikipedia_id_triple # todo integrate these as well
]
        if i==1:
            break

    print send_to_db.send_to_db(triples[:len(triples)])
    print len(triples)
