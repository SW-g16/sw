# SPARQL Queries

## Endpoints:
### 1. http://data.consilium.europa.eu/sparql
  1. **Get the act and what each country voted on said act:**

```
PREFIX eucodim: <http://data.consilium.europa.eu/data/public_voting/qb/dimensionproperty/>
PREFIX eucoprop: <http://data.consilium.europa.eu/data/public_voting/qb/measureproperty/>
PREFIX eucovote: <http://data.consilium.europa.eu/data/public_voting/consilium/vote/>

SELECT ?act ?country ?vote
from <http://data.consilium.europa.eu/id/dataset/votingresults>
where {
  ?observation eucodim:country ?country .
  ?observation eucoprop:vote ?vote .
  ?observation eucodim:act ?act .
}
ORDER BY DESC(?act)
```
