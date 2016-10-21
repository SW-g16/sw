
STARDOG_SERVER = 'http://localhost:5820/'  # you must have stardog running here
DB_NAME = 'votes'  # you must have a db with this name at ENDPOINT. NB also change reset-db.sh upon changing this var
ENDPOINT = STARDOG_SERVER + DB_NAME

WEBSITE = 'votes.example.com'  # arbitrary

DB_NS = 'v'  # arbitrary
DB_PREFIX = 'http://' + WEBSITE + '/' + DB_NS + "/" # arbitrary

GT_NS = 'gt' # arbitrary
GT_PREFIX = 'https://www.govtrack.us/api/v2/' # must point to govtrack api v2