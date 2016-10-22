import os

MAX_ACTIVE_THREADS = 8
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/data/govtrack-data/congress/' # the location of the downloaded bulk data, relative from where you call this script
VOTE_PROPERTIES = [':votesYay', ':votesNay', ':abstain']
VOTE_KEYS = ['Yea', 'Nay', 'Not Voting']
EMPTY_THRESHOLD = 1500
