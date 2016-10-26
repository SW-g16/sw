import os

PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # the location of the downloaded bulk data
DATA_PATH = PATH + '/data'
CONGRESS_PATH = DATA_PATH + '/govtrack/congress/'

EMPTY_THRESHOLD = 1500

BASE_URI = 'http://localhost:5820/databases/votes/'

print PATH
print DATA_PATH

PREFIX = 'votes'

VOTE_VOC = {'Yea': ':upvotes', 'Nay': ':downvotes', 'Not Voting': ':abstains'}

PROP_BILL_TEXT = PREFIX+':hasText'
PROP_PROCESSED_BY = PREFIX+':processedBy'
PROP_WIKIPAGE = PREFIX+':wikipedia'
PROP_PARTY = 'dbr:party'
PROP_SAMEAS = 'owl:sameAs'
PROP_LAST_NAME = 'foaf:lastName'
PROP_FIRST_NAME = 'foaf:firstName'

URI_USA_SENATE = 'dbr:United_States_Senate'
URI_USA_HOUSE = 'dbr:United_States_House_of_Representatives'

NS_OURS = '<http://localhost:5820/databases/votes/>'
NS_DBR = '<http://dbpedia.org/resource/>'
NS_OWL = '<http://www.w3.org/2002/07/owl#>'
NS_FOAF = '<http://xmlns.com/foaf/0.1/>'