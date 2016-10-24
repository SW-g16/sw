from flask import json


def load_json(path):
    f = open(path, 'r')
    print 'Loading file:', path
    print '(This will take a while)'
    json_data = json.load(f)
    f.close()
    return json_data
