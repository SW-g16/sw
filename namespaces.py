
URI_USA_SENATE = 'dbr:United_States_Senate'
URI_USA_HOUSE = 'dbr:United_States_House_of_Representatives'


VOTES = 'votes'
DBO = 'dbo'
DBR = 'dbr'
OWL = 'owl'
FOAF = 'foaf'

NAMESPACES = {
    VOTES:'http://localhost:5820/databases/votes/',
    DBO:'http://dbpedia.org/ontology/',
    DBR:'http://dbpedia.org/resource/',
    OWL:'http://www.w3.org/2002/07/owl#',
    FOAF:'http://xmlns.com/foaf/0.1/'
}


PREFIX_LINES = '\n'.join(['@prefix %s: <%s>.' % (key, NAMESPACES[key]) for key in NAMESPACES])

from rdflib import Namespace, XSD

ONT = Namespace('http://localhost:5820/databases/votes/')
DOSSIER_TYPE = 'Legislative proposal published'
DBO = Namespace('http://dbpedia.org/ontology/')
DBR = Namespace('http://dbpedia.org/resource/')
DBP = Namespace('http://dbpedia.org/property/')
DOSSIER = ONT['Bill']
DOSSIER_TITLE = ONT['bill_text']
PROCESSED_BY = ONT['processedBy']
ABSTAINS = ONT['abstains']
VOTES_FOR = ONT['upvotes']
VOTES_AGAINST = ONT['downvotes']
PARTY = DBO['party']
EUROPEAN_PARLIAMENT = DBR['European_Parliament']
IN_LEGISLATURE = DBO['politicalPartyInLegislature']
OFFICE = DBP['office']
MEMBER_OF_EU = DBR['Member_of_the_European_Parliament']
THUMBNAIL = DBO['thumbnail']
BIRTH_DATE = DBO['birthDate']
BIRTH_PLACE = DBO['birthPlace']
DEATH_DATE = DBO['deathDate']
DATE = XSD['date']






