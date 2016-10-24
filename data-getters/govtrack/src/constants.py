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
