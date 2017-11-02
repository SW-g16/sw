from flask import Flask, render_template, request
import sys

assert len(sys.argv)==2, 'bad arguments, usage: %s <database_name>' % sys.argv[0]
ENDPOINT = 'http://localhost:5820/%s/query'
DB_NAME = sys.argv[1]

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

@app.route('/parties')
def parties():
    import os
    filename = os.path.join(os.path.dirname(__file__)+ '/../queries/party_statistics_across_bills.rq')
    with file(filename) as f: query = f.read()
    results = get_data(ENDPOINT % DB_NAME, query)
    stats = results['results']['bindings']
    parties = {}
    for row in stats:
        print row
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
    return render_template('parties.html',data=parties)


@app.route('/party',methods=['GET'])

def party():

    party = request.args.get('party')
    query = """

        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbp: <http://dbpedia.org/property/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX votes: <http://localhost:5820/databases/votes/>

          select distinct

                # target values
                ?assembly
                ?bill
                ?bill_date
                ?bill_text
                ?yes_members
                ?no_members
                ?abstain_members

                # the degree of uniformity, by some measure. is 0 if 50/50, is 1 if all voted in same direction
                ((abs(?yes_members-?no_members)/(?yes_members+?no_members)) as ?uniformity)
                ((?abstain_members/(?yes_members + ?no_members + ?abstain_members)) as ?abstain_proportion)
                # ((?yes_members + ?no_members + ?abstain_members) / ?voters as ?party_rep_proportion )

          where {

              select distinct

                    # target values
                    ?assembly
                    ?bill
                    ?bill_date
                    ?bill_text
                    # the number of voters who voted for the target bill
                    # to heavy # (count(?voter_4) as ?voters)

                    # the number of members of the target party who voted in each direction
                    (count(distinct ?voter_1) as ?yes_members)
                    (count(distinct ?voter_2) as ?no_members)
                    (count(distinct ?voter_3) as ?abstain_members)

              where {

                    # we only consider bills of the target assembly
                    ?bill votes:processedBy ?assembly.

                    # the date of the bill's voting event
                    ?bill xsd:date ?bill_date.

                    # the bill's text
                    ?bill votes:bill_text ?bill_text.

                    # we only consider voters that are member of the target party
                    ?voter_1 dbo:party <""" + party + """>.
                    ?voter_2 dbo:party <""" + party + """>.
                    ?voter_3 dbo:party <""" + party + """>.

                    # we identify upvoters, downvoters, and abstainers
                    ?voter_1 votes:upvotes ?bill.
                    ?voter_2 votes:downvotes ?bill.
                    ?voter_3 votes:abstains ?bill.

                    # any voter that voted for this bill
                    # too heavy # ?voter_4 votes:votesOn ?bill.

              }
              group by ?bill ?party_members ?assembly ?bill_date ?bill_text # ?voters
          }
          group by ?assembly ?bill ?yes_members ?no_members ?abstain_members ?bill_date ?bill_text # ?voters
          order by desc(?bill_date)

"""
    print query
    results = get_data(ENDPOINT % DB_NAME, query)
    stats = results['results']['bindings']
    party_history = []
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
                try:
                    party_view[str(key)] = str(row[key]['value'])
                except:
                    print 'tried with' , key, str(key), row[key], row[key]['value']
        party_history.append(party_view)

    return render_template('party.html', data=party_history,party_uri=party)


if __name__ == '__main__':
    app.debug = True
    app.run()
