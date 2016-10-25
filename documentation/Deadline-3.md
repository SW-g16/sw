## Deadline 3

## External Sources (100-200 words)
Our three primary external sources are govtrack.us, www.europarl.europa.eu and
http://data.consilium.europa.eu/id/dataset/votingresults , which contain the 
voting results for the United States Parliament, the European Parliament and 
the European Council respectively. In addition, we also make use of DBPedia for 
acquiring additional information about politicians and countries in our 
ontology. 

## Motivation for using these sources (100-200 words)
We considered a great many parliamentary databases during the course of our 
product. Our first intention was of course to integrate the Netherlands, but 
that turned out to not be very feasible due to not having an endpoint or 
organized data source for parliamentary votes available. We next investigated 
the US data at govtrack.us, which turned out to be a perfect data source for 
this project due being expansive, consistent and easily accessible. It thus 
formed the basis of much of our early ontology. Finding another source took us a
long time, and we went through several other endpoints, including an attempt to 
integrate the data of the UK house of commons. We eventually settled on using 
the respective data sets of the EU council and parliament. The council dataset 
was somewhat limited in its scope compared to the more exhaustive govtrack and 
eu parliament sets, but was still suitable for our purpose.

## Description how you integrated the data (200-300 words)
In our ontology, we speak of four classes as being central: Voters, Bills, 
Assembly and Polity. Voter and Bills are found in the contents of the datasets
we mined. Assembly and Polity are determined by which dataset the data comes
from. 

## SPARQL Queries (200-300 words)



## Discussion and evidence of inference (200-300)