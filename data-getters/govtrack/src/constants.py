import os

PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # the location of the downloaded bulk data
DATA_PATH = PATH + '/data'
CONGRESS_PATH = DATA_PATH + '/govtrack/congress/'
VOTE_VOC = {'Yea': ':votesYay', 'Nay': ':votesNay', 'Not Voting': ':abstains'}

EMPTY_THRESHOLD = 1500

BASE_URI = 'http://votes.example.com/ontology/'

print PATH
print DATA_PATH



PROP_BILL_TEXT = ':hasText'
PROP_PROCESSED_BY = ':processedBy'
PROP_LAST_NAME = 'foaf:lastName'
PROP_FIRST_NAME = 'foaf:firstName'
PROP_MEMBEROF = ':memberOf'
PROP_SAMEAS = 'owl:sameAs'
PROP_WIKIPAGE = ':wikipedia'

URI_USA_SENATE = 'dbr:United_States_Senate'
URI_USA_HOUSE = 'dbr:United_States_House_of_Representatives'

NS_OURS = '<http://votes.example.com/ontology/>'
NS_DBR = '<http://dbpedia.org/resource/>'
NS_OWL = '<http://www.w3.org/2002/07/owl#>'
NS_FOAF = '<http://xmlns.com/foaf/0.1/>'