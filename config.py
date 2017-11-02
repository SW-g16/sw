import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

ONTOLOGY_PATH = '%s/ontology.ttl' % ROOT_DIR

DATABASE_NAME = 'sw'

TRIPLES_PER_UPLOAD = 10000
