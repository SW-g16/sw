import govtrack #, more scripts for more sources
import requests

triple_sets = [
    govtrack.constructData()
    # , othersource.constructData()
]

def storeTriples(triples):

    endpoint = "http://localhost:5820/votes"

    def to_rdf(triples):
        rdf_str = "@prefix v: <http://votes.example.com/ontology/>. \n"
        for t in triples:
            rdf_str += t[0]+" "+t[1]+" "+t[2]+ ". \n"
        return rdf_str

    data = to_rdf(triples)
    # print data # this should output valid turtle. validate at http://www.easyrdf.org/converter
    return requests.post('http://localhost:5000/store',data={'data':data})


for i in triple_sets:
    print storeTriples(i)