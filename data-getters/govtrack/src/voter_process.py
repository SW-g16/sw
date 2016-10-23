
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
2   foaf:gender
4   :votesIn dbr:United_States_House_of_Representatives | :votesIn dbr:United_States_Senate
5   :respresentsState dbr:Mississippi // however we get only the acronym. we use the map ross linked to to get the whole name
7   :memberOf dbr:Republican_Party_(United_States)
18  :sameAs <uri_generated_by_votes_getter/bioguide_id>  // <-- indicate equality with already stored voter
23  :<http://www.govtrack.us/api/v2/person/govtrack_id>  // <-- the main uri for our voter
28  :wikipedia <http://www.wikipedia.org/wiki/wikipedia_id>

"""
import os

path = os.path.dirname(os.path.realpath(__file__))+'/../../../data/govtrack/congress-legislators/legislators-current.csv'

import csv

with open(path, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    headers = []
    i=0
    for row in spamreader:
        if i==0:
            headers = row
            i=1
            print headers
            continue
        print row
        #
        break