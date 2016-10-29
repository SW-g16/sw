
import os

PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))) + '/sw'

DATA_PATH = PATH + '/data/govtrack/'
CONGRESS_PATH = DATA_PATH + 'congress/'
print CONGRESS_PATH

BASE_URI = 'http://localhost:5820/databases/votes/'

PREFIX = 'votes'

VOTE_VOC = {'Yea': PREFIX+':upvotes', 'Nay': PREFIX+':downvotes', 'Not Voting': PREFIX+':abstains'}

PROP_BILL_TEXT = PREFIX+':bill_text'
PROP_BILL_DATE = PREFIX+':bill_date'
PROP_PROCESSED_BY = PREFIX+':processedBy'
PROP_WIKIPAGE = PREFIX+':wikipedia'
PROP_PARTY = 'dbo:party'
PROP_SAMEAS = 'owl:sameAs'
PROP_NAME = 'foaf:name'
URI_USA_SENATE = 'dbr:United_States_Senate'
URI_USA_HOUSE = 'dbr:United_States_House_of_Representatives'

NS_OURS = '<http://localhost:5820/databases/votes/>'
NS_DBO = '<http://dbpedia.org/ontology/>'
NS_DBR = '<http://dbpedia.org/resource/>'
NS_OWL = '<http://www.w3.org/2002/07/owl#>'
NS_FOAF = '<http://xmlns.com/foaf/0.1/>'
