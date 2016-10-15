from flask import Flask, render_template, request

import constants as c

from SPARQLWrapper import SPARQLWrapper
from flask import json

app = Flask(__name__)


def get_data(endpoint):
    # TODO figure why stardog returns all triples of the db upon this query
    # this bug(?) is a bottleneck for progress

    q = """
        PREFIX votes: <http://www.votes.example.com/votes/>
        select distinct ?voter ?bill ?stance where {
            ?voter ?bill ?stance .
            FILTER (?stance=1 || ?stance=-1 || ?stance=0)
        }
        """

    s = SPARQLWrapper(endpoint)
    s.setQuery(q)
    s.setReturnFormat('rdf')
    s.addParameter('Accept', 'application/sparql-results+json,')
    #  s.addParameter('reasoning', 'true')
    r = s.query().convert()
    return json.dumps(r)


@app.route('/')
def first_page():
    return render_template('index.html')

@app.route('/display')
def display():
    r = get_data(c.ENDPOINT)
    return render_template('display.html', result=r, db_prefix=c.DB_PREFIX, db_ns=c.DB_NS, gt_ns=c.GT_NS,
                           gt_prefix=c.GT_PREFIX)


@app.route('/store', methods=['POST'])
def store():
    import put
    return put.store(c.ENDPOINT, request.form['data'].encode('utf-8'))


if __name__ == '__main__':
    app.debug = True
    app.run()
