import requests

# todo figure how to avoid duplicating this file


def send_to_db(triples):
    rdf = '.\n'.join(["%s %s %s" % (t[0], t[1], t[2]) for t in triples if len(t) == 3]) + '.'
    #    print rdf
    return requests.post('http://localhost:5000/store', data={'data': rdf})
