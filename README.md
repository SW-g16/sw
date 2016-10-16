# Sem Web G16 Implementation

Using LD-R

## Installation

1. clone the repository and its submodules:
```
git clone https://github.com/Ysgorg/sw.git
cd sw
git submodule init
git submodule update
```
2. make sure you have stardog installed
3. run /scripts/start.sh and follow the instructions (chmod 750 start.sh if you get permission denied)
4. Open LD-R in your browser (localhost Port 3000 for dev mode, 4000 for build mode), click datasets -> votes. You should now see the data of ontology.ttl!

## About

This is a project revolving around the semantic organization and
presentation of voting data from different endpoints.

## Choice of framework

 - Lets us use existing ui components for semantic data
 - If we produce a useful application, it will be easier for others to reuse it
 - LD-R is generally awesome

## Status, considerations, design notes

These are things and decisions that need to done and taken

### Ontology

A minimal voting ontology is given as `ontology.ttl` upon initial commit.
It tells us that Voters abstain or vote yay or nay to Bills.
This can be expanded both for Bills and Voters.
Voters can belong to parties, bills, have dates, etc

### Inference

LD-R displays Stardog's inferred knowledge that v:bob is a owl:Thing.
Woo!

### Deduction

We want to deduce plotable numbers of interest from our dataset.
This can (should?) be done with sparql.

### Data Flow

Store copies of external data or query external data in real-time?

### Visualization

look for existing ld-r components for visualization.
if we don't find what we want, we can make some
within the ld-r framework.

What do we want to visualize exactly, and how?

 - network graphs (of what?)
 - plots (statistics over time)

look for visualizations of other political data for inspiration

### Data acquisition

Endpoints arent uniform. This is among the problems of web 2.0 and motivation for semantic web.
We'll need to do some custom coding for new endpoints.
Different endpoints have different numbers of timbl-stars.
We are very happy when states provide 5-star data
 - particularly if the 5th star is earned by using a shared vocabulary for votes.
This would let us use access several datasets with a single alignment.
In less fortunate cases, we get 3-star data.
We can still construct rdf data with json and csv, but we won't go lower.
