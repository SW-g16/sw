MAX_ACTIVE_THREADS = 8
CONGRESS_PATH = 'govtrack-data/data/congress/'  # the location of the downloaded bulk data, relative from where you call this script
VOTE_PROPERTIES = [':votesYay', ':votesNay', ':abstains']
VOTE_KEYS = ['Yea', 'Nay', 'Not Voting']
EMPTY_THRESHOLD = 1500

BASE_URI = 'http://votes.example.com/ontology/'
