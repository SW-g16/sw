#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, jsonify
from SPARQLWrapper import SPARQLWrapper, RDF, JSON
import json
import requests
import traceback

app = Flask(__name__)

ENDPOINT = 'http://localhost:5820/'  # you must have stardog running here
DB_NAME = 'votes'  # you must have a db with this name at ENDPOINT. NB also change reset-db.sh upon changing this var
DB_NS = 'v'  # arbitrary
WEBSITE = 'votes.example.com'  # arbitrary


def query_our_db(query):
    s = SPARQLWrapper(ENDPOINT + DB_NAME)
    s.setQuery(query)
    s.setReturnFormat('rdf')
    s.addParameter('Accept', 'application/sparql-results+json,')
    s.addParameter('reasoning', 'true')
    return json.dumps(s.query().convert())


@app.route('/display', methods=['GET'])
def display():
    q = \
        'select ?uri ?text where {?uri a hume:Law.?uri hume:stringified ?text.} limit 5'
    r = query_our_db(q)
    return render_template('display.html', result=r,
                           store_endpoint=ENDPOINT + DB_NAME,
                           website=WEBSITE, db_name=DB_NAME)


@app.route('/')
def first_page():
    app.logger.debug('You arrived at ' + url_for('first_page'))
    return render_template('index.html')


@app.route('/import')
def import_():
    app.logger.debug('You arrived at ' + url_for('import_'))
    return render_template('import.html', store_endpoint=ENDPOINT,
                           db_ns=DB_NS, db_name=DB_NAME,
                           website=WEBSITE)


@app.route('/sparql', methods=['GET'])
def sparql():
    app.logger.debug('You arrived at ' + url_for('sparql'))
    app.logger.debug('I received the following arguments'
                     + str(request.args))

    endpoint = request.args.get('endpoint', None)
    query = request.args.get('query', None)

    return_format = request.args.get('format', 'RDF')

    if endpoint and query:
        s = SPARQLWrapper(endpoint)

        s.setQuery(query)

        if return_format == 'RDF':
            s.setReturnFormat(RDF)
        else:
            s.setReturnFormat(JSON)
            s.addParameter('Accept',
                                'application/sparql-results+json')

        s.addParameter('reasoning', 'true')

        app.logger.debug('Query:\n{}'.format(query))

        app.logger.debug('Querying endpoint {}'.format(endpoint))

        try:
            response = s.query().convert()

            app.logger.debug('Results were returned, yay!')

            app.logger.debug(response)

            if return_format == 'RDF':
                print response
                app.logger.debug('Serializing to Turtle format')
                return response.serialize(format='turtle')
            else:
                app.logger.debug('Directly returning JSON format')
                return jsonify(response)
        except Exception, e:
            app.logger.error('Something went wrong')
            traceback.print_exc()
            return jsonify({'result': 'Error'})
    else:

        return jsonify({'result': 'Error'})


@app.route('/store', methods=['POST'])
def store():
    app.logger.debug('You arrived at ' + url_for('store'))
    app.logger.debug('I received the following arguments'
                     + str(request.form))

    data = request.form['data'].encode('utf-8')

    transaction_begin_url = ENDPOINT + DB_NAME + '/transaction/begin'
    app.logger.debug('Doing a POST of your data to {}'.format(transaction_begin_url))

    # Start the transaction, and get a transaction_id

    response = requests.post(transaction_begin_url,
                             headers={'Accept': 'text/plain'})
    transaction_id = response.content
    app.logger.debug(response.status_code)

    # POST the data to the transaction

    post_url = ENDPOINT + DB_NAME + '/' + transaction_id + '/add'
    app.logger.debug('Assuming your data is Turtle!!')
    response = requests.post(post_url, data=data,
                             headers={'Accept': 'text/plain',
                                      'Content-type': 'text/turtle'})
    app.logger.debug(response.status_code)
    app.logger.debug(response.content)
    app.logger.debug(response.headers)

    if response.status_code != 200:
        return str(response.content)

    # Close the transaction

    transaction_close_url = ENDPOINT + DB_NAME + '/transaction/commit/' \
                            + transaction_id
    response = requests.post(transaction_close_url)
    app.logger.debug(response.status_code)
    app.logger.debug(response.content)
    app.logger.debug(response.headers)

    if response.status_code != 200:
        return str(response.content)
    else:
        return 'Ok!'

if __name__ == '__main__':
    app.debug = True
    app.run()

			