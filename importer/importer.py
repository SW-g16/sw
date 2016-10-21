import govtrack #, more scripts for more sources
import requests

triple_sets = [
    govtrack.constructData()
    # , othersource.constructData()
]

def storeTriples(triples):
    rdf = [t[0]+" "+t[1]+" "+t[2]+ ". \n" for t in triples]
    return requests.post('http://localhost:5000/store',data={'data':rdf})

for i in triple_sets:
   # print storeTriples(i)
    pass