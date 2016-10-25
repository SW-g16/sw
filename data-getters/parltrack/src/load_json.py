from flask import json

def load_json(path):
    try:
        f = open(path, 'r')
        print 'Loading file:', path
        try:
            json_data = json.load(f)
        except ValueError, error:
            print error
            print
            return None
        f.close()
        print
        return json_data
    except IOError, error:
        print error
        print
        return None