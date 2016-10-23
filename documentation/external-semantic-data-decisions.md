# External Semantic Data Decisions

External data on our domain is available. 

Among our [goals](final-report.md#goals) is this: 

> Provide an endpoint combining open voting data from different sources

Here, 'combining' is ambiguous. 

In any interpretation, we need to at least have a way to view data of external origin through our vocabulary. 
This requires, at some location, that we have a path of interpretation between our and external formats.
The first data source we made this condition true for is Govtrack.us' open data. 
It is in JSON format, and the bulk data is organized in a large amount of small json files within several layers of folders. 

We integrated the data by running a custom interpreter on it. 
Written in python, it iterated through the folders and picked out the interesting data. 
After a complete processing (still not done), the govtrack data can be deleted. 
We also have exactly all the triples we wanted from the source, expressed through our vocabulary. 

An alternative to this is to never store any data, but instead query external sources and perform analysis in real-time, as users enter queries. 

Arguments for this (chat dump):
    (tried mining arguments from convo but difficult)

Other arguments for:
 - Saves us approximately ??? mb per datatype
 - We will still be providing new semantic data

Arguments against:
 - will decrease query time performance
 - would be significant avoidable computational cost for open data provider
 - will not affect the level of semantic integration with other sources
 - the pre-processing time is on the tolerable scale of < 4 hours per dataset (todo test this with full import test). 
 