# TODO's

This document is intended to help guide our efforts.
If you don't know what to do, you can pick a task from here.
If there's something that should be done but isn't written here, please write it.

## Urgent (next deadline)

### Domain Modelling Docs

They need to be written.

### Fixing/Improving Ontology
- Rename reactsToVote to reactsToBill
- Refactor demographics classes to subclasses of Person (make our own person class and map to DBO:Person?)
- Fix memberOf <Party> so that it's not longer an annotation but an object referring to a subclass of Party
- Get gender from govtrack
- Map another dataset (EU, UK, ?)
- Make more inferences

## Less urgent (after next deadline)

### Redesign Importer

The current data getter makes an avoidable large amount of queries for a task that is intended to be rarely performed. 
It is currently useful as an api, if we just want a small subset of govtrack's data. 
But we want all the data, and users will be accessing data often. 

So, we should consider downloading the data in bulk and hosting it ourselves. 
This would also be polite to the source data provider. 

### Another Data Importer

We should have at least two data getters. Two is enough to force us to handle data from a set of datasets (rather than one) and to have a modular data-getter code base and to show we can align diversely formatted data.

### Data View Configuration in LD-R

We want to configure the views of our data.
For instance, we want to output that voters are a v:Voter,
but not that they are a owl:Thing. Where/how to configure this?

### Computing Statistics

We want to compute, cache and display statistics (such as proportion of democrats who votes yes on this bill). Where/how?

# Resolved Issues

## Inference Issue
Stardog register our voters as `owl:Thing`s, while we want it to be inferred that they are `v:Voter`s. This needs to be resolved, so we can "show evidence of meaningful inference". Error in ontology? Stardog? Database config?
