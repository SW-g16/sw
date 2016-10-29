import traceback
from pprint import pprint

from flask import Flask, render_template, request, jsonify

import constants as c

from SPARQLWrapper import SPARQLWrapper
from flask import json

app = Flask(__name__)


def get_data(endpoint,query):

    from SPARQLWrapper import SPARQLWrapper, JSON

    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

@app.route('/')
def first_page():
    return render_template('index.html')

@app.route('/statistics')
def statistics():
    import os
    filename = os.path.join(os.path.dirname(__file__)+ '/../queries/party_statistics_across_bills.rq')
    with file(filename) as f: query = f.read()
    results = get_data(c.ENDPOINT,query)
    stats = results['results']['bindings']
    parties = {}
    for row in stats:
        party_view = {}
        for key in row:
            print row[key]
            if 'datatype' in row[key]:
                if row[key]['datatype'] == u'http://www.w3.org/2001/XMLSchema#integer':
                    party_view[str(key)] = int(row[key]['value'])
                elif row[key]['datatype'] == u'http://www.w3.org/2001/XMLSchema#decimal':
                    party_view[str(key)] = float(row[key]['value'])
                else:
                    party_view[str(key)] = str(row[key]['value'])

            else:
                party_view[str(key)] = str(row[key]['value'])
        uri = party_view['party']
        del party_view['party']
        parties[uri] = party_view
    return render_template('statistics.html',data=parties)


@app.route('/bill',methods=['GET'])
def bill():

    bill = request.args.get('bill')
    query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX votes: <http://localhost:5820/databases/votes/>

        select (count(?yes_voter) as ?yes_voters) (count(?no_voter) as ?no_voters) (count(?abstainer) as ?abstainers)
        where {
            ?yes_voter votes:upvotes <""" + bill + """>.
            ?no_voter votes:downvotes <""" + bill + """>.
            ?abstainer votes:abstains <""" + bill + """>.
        }"""
    results = get_data(c.ENDPOINT,query)
    stats = results['results']['bindings']
    party_history = {}
    for row in stats:
        party_view = {}
        for key in row:
            print row[key]
            if 'datatype' in row[key]:
                if row[key]['datatype'] == u'http://www.w3.org/2001/XMLSchema#integer':
                    party_view[str(key)] = int(row[key]['value'])
                elif row[key]['datatype'] == u'http://www.w3.org/2001/XMLSchema#decimal':
                    party_view[str(key)] = float(row[key]['value'])
                else:
                    party_view[str(key)] = str(row[key]['value'])

            else:
                party_view[str(key)] = str(row[key]['value'])
        uri = party_view['party']
        del party_view['party']
        party_history[uri] = party_view

    return render_template('bill.html', data=view)


if __name__ == '__main__':
    app.debug = True
    app.run()
