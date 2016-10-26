# SPARQL Queries

## Endpoints:
### 1. http://localhost:5820/votes/query
```
select ?bill (COUNT(distinct ?voter_1) as ?nay_votes) (COUNT(distinct ?voter_2) as ?yay_votes) (COUNT(distinct ?voter_3) as ?abstains)
where {

	?voter_1 votes:downvotes ?bill.
	?voter_2 votes:upvotes ?bill.
	?voter_3 votes:abstains ?bill.
}
GROUP BY ?bill
```

```
select ?bill (COUNT(distinct ?voter_1) as ?downvotes) (COUNT(distinct ?voter_2) as ?upvotes) (COUNT(distinct ?voter_3) as ?abstains) (?downvotes + ?upvotes + ?abstains as ?totalVotes)
where {
	?voter_1 votes:downvotes ?bill.
	?voter_2 votes:upvotes ?bill.
	?voter_3 votes:abstains ?bill.
}
GROUP BY ?bill
ORDER BY ?totalVotes
```

### 2. http://data.consilium.europa.eu/sparql
  1. **Get the act and what each country voted on said act:**

```
PREFIX eucodim: <http://data.consilium.europa.eu/data/public_voting/qb/dimensionproperty/>
PREFIX eucoprop: <http://data.consilium.europa.eu/data/public_voting/qb/measureproperty/>
PREFIX eucovote: <http://data.consilium.europa.eu/data/public_voting/consilium/vote/>

SELECT (STR(?actnumber) as ?actnumber) (STR(?description) as ?description) (STR(?countryName) as ?countryName) (STR(?voted) as ?voted)
from <http://data.consilium.europa.eu/id/dataset/votingresults>
where {
  ?observation eucodim:country ?country .
  ?observation eucoprop:vote ?vote .
  ?observation eucodim:act ?act .
  ?country <http://www.w3.org/2004/02/skos/core#prefLabel> ?countryName .
  ?vote <http://www.w3.org/2004/02/skos/core#prefLabel> ?voted .
  ?act <http://www.w3.org/2004/02/skos/core#definition> ?description .
  ?act <http://www.w3.org/2004/02/skos/core#prefLabel> ?actnumber .
}
ORDER BY DESC(?act)
```

# As far as I can tell, there is no place in the endpoint that says whether the act passed, the number of votes per country (by which we could have calculated it ourselves)*, or full description of acts.

# * it does interlink with dbpedia, but that doesn't have the info either
