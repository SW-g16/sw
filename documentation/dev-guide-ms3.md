<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Development Guide for Milestone 3](#development-guide-for-milestone-3)
  - [Raw Assignment Description](#raw-assignment-description)
  - [Practical Requirements](#practical-requirements)
    - [Incoporate external data](#incoporate-external-data)
    - [Deliver Working Prototype](#deliver-working-prototype)
  - [Documentation Skeleton](#documentation-skeleton)
    - [External Data Sources](#external-data-sources)
      - [Review of Data Sources](#review-of-data-sources)
      - [Choice of Data Sources](#choice-of-data-sources)
    - [Integration methodology](#integration-methodology)
    - [Querying](#querying)
      - [Relevant Complex SPARQL Queries](#relevant-complex-sparql-queries)
      - [Query Results Discussion](#query-results-discussion)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Development Guide for Milestone 3

*This doc is intended to help us get going early for the next deadline. Empty checkboxes are todo's that aren't done yet. Some subtasks remain unidentified. See also todo.md, for todo's not required for the next deadline.*

 - [ ] identify all tasks, denote them like this

## Raw Assignment Description

For this milestone, you need to incorporate external data, and deliver a working prototype of your application.
In separate sections, provide the following:

 1. a description of at least 2 external sources of data that will be used by your application. At least one of these must be an external SPARQL endpoint. The other dataset need not be in RDF. (100-200 words)
 2. a motivation for choosing these data sources: why does the application need these sources specifically. (100-200 words)
 3. a description of how you produce integrated the data with your ontology, did you use inferencing? (200-300 words)
 4. a description of multiple complex SPARQL queries, relevant for the application, that produce results over the integrated data and ontology (200-300 words)
 5. a description and evidence that running the SPARQL queries against the ontology and data produces inferences (screenshot reasoning on/off). Discuss the inferences. (200-300 words)
 6. Have a working prototype of the application (nothing to hand in)
 7. Combine this with a revised version of milestones 1 and 2.

Within the final report, these sections correspond to the rubrics Data reuse and Queries. Together these determine 20 out of 90 points. 

## Practical Requirements

### Incoporate external data

We must incorporate external data to our application. We've already achieved this for one data source, but need to incorporate at least one more as well. For the datasource that we're already accessing data from: we should host the data ourselves, downloading it in bulk (to be nice to provider). 

 - [ ] import one more data source 
 - [ ] download bulk data for govtrack

### Deliver Working Prototype

This is already achieved on at least one system. However we need to be able to replicate the setup in which everything works. 

 - [ ] replicate working setup. running our scripts on a fresh f.ex. Ubuntu 14.04 should yield a working, running application with all external data imported to our database, browsable in LD-R.  

## Documentation Skeleton 

### External Data Sources

#### Review of Data Sources

> Describe at least 2 external data sources used by our application. At least one of these must be an external SPARQL endpoint. 100-200 words. 
 
 - [ ] put the table of data sources here, and fill it with more datasets

#### Choice of Data Sources 

> Give motivation for choosing the data sources. Why these sources, specifically? 
 
 - [ ] choose a subset of the candidate data sources to use (for now. may indefinetly expand with more datasets later)

### Integration methodology

> Describe how we integrated the data with your ontology. Inferencing? 200-300 words.

### Querying

#### Relevant Complex SPARQL Queries

> Description multiple complex SPARQL queries relevant to the application, that produce results over the integrated data and ontology. 200-300 words.

#### Query Results Discussion

> a description and evidence that running the SPARQL queries against the ontology and data produces inferences (screenshot reasoning on/off). Discuss the inferences. (200-300 words)
