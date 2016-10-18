# TODO's

This document is intended to help guide our efforts. Don't know what to do? Look here. 

## Urgent (next deadline)

### Inference Issue

Stardog register our voters as `owl:Thing`s, while we want it to be inferred that they are `v:Voter`s. This needs to be resolved, so we can "show evidence of meaningful inference". Error in ontology? Stardog? Database config? 

### Domain Modelling Docs

They need to be written. 

## Less urgent (after next deadline)

### Another Data Getter

We should have at least two data getters. Two is enough to force us to handle data from a set of datasets (rather than one) and to have a modular data-getter code base and to show we can align diversely formatted data. 

### Data View Configuration in LD-R

We want to configure the views of our data. Where/how?

### Computing Statistics

We want to compute, cache and display statistics (such as proportion of democrats who votes yes on this bill). Where/how?