* upvotes
```
PREFIX eucodim: <http://data.consilium.europa.eu/data/public_voting/qb/dimensionproperty/>
PREFIX eucoprop: <http://data.consilium.europa.eu/data/public_voting/qb/measureproperty/>
PREFIX eucovote: <http://data.consilium.europa.eu/data/public_voting/consilium/vote/>
PREFIX votes: <http://localhost:5820/databases/votes/>

CONSTRUCT {
  ?country votes:upvotes ?act .
  ?act votes:bill_text ?description .
}
FROM <http://data.consilium.europa.eu/id/dataset/votingresults>
WHERE {
  ?observation eucodim:country ?country .
  ?observation eucoprop:vote eucovote:votedinfavour .
  ?observation eucodim:act ?act .
  ?act <http://www.w3.org/2004/02/skos/core#definition> ?description .
}
```

* downvotes
```
PREFIX eucodim: <http://data.consilium.europa.eu/data/public_voting/qb/dimensionproperty/>
PREFIX eucoprop: <http://data.consilium.europa.eu/data/public_voting/qb/measureproperty/>
PREFIX eucovote: <http://data.consilium.europa.eu/data/public_voting/consilium/vote/>
PREFIX votes: <http://localhost:5820/databases/votes/>

CONSTRUCT {
  ?country votes:downvotes ?act .
  ?act votes:bill_text ?description .
}
FROM <http://data.consilium.europa.eu/id/dataset/votingresults>
WHERE {
  ?observation eucodim:country ?country .
  ?observation eucoprop:vote eucovote:votedagainst .
  ?observation eucodim:act ?act .
  ?act <http://www.w3.org/2004/02/skos/core#definition> ?description .
}
```

* abstains
```
PREFIX eucodim: <http://data.consilium.europa.eu/data/public_voting/qb/dimensionproperty/>
PREFIX eucoprop: <http://data.consilium.europa.eu/data/public_voting/qb/measureproperty/>
PREFIX eucovote: <http://data.consilium.europa.eu/data/public_voting/consilium/vote/>
PREFIX votes: <http://localhost:5820/databases/votes/>

CONSTRUCT {
  ?country votes:abstains ?act .
  ?act votes:bill_text ?description .
}
FROM <http://data.consilium.europa.eu/id/dataset/votingresults>
WHERE {
  ?observation eucodim:country ?country .
  ?observation eucoprop:vote eucovote:abstained .
  ?observation eucodim:act ?act .
  ?act <http://www.w3.org/2004/02/skos/core#definition> ?description .
}
```
