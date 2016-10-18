/*
    this is a stub for tomorrow's delivery. 
    everything in java-style comments are comments for us, 
    everything else is part of the doc as we deliver it
*/

# Domain Modelling

Group 16
// names

## Domain and Scope

// 100-200 words

// Description of the domain and scope of the ontology, as determined by the application 

// what's the difference between domain and scope?

Our domain is voting data of official voting assemblies of different countries. 
We map votes, voters and voting assembly compositions through time. 
Relevant data is provided by different official actors and is in different formats, 
    and does not currently exist in a combined ontology. 
This means both that we have to hand-write aligners/mappers/getters for each different data source, 
    and that our application will result in production of useful semantic data. 
    
### Required Domain Knowledge

All we need is a basic understanding of voting processes and institutions:
voters vote for bills in voting assemblies, and the bills that are passed
are applied to some polity. 

### Possible Domain Extentions

#### Election and Polling Data

We could combine our data with election results and inter-election polls. 
This would allow us to compute more interesting measures, 
    such as how close voting assembly compositions are to 
    the population's desired composition at a digen point in time

## Ontology Construction Methodology

// 100-200 words

// Description of the methodology that is used in the construction of the ontology 

// methodology? we opened protege, then clicked stuff until we were done

We constructed an ontology able to express the information we're interested in
(generally outlined under Domain and Scope, detailed in Conceptualization).
For the practical task of constructing the ontology, we used Protege. 

## Conceptualization

// 200-300 words

// Conceptualization of the domain (concepts, relations) described, discussed and depicted in a drawing. 
// The conceptualization should encompass more than 15 classes and at least 5 properties 


### Our Concepts

These are the concepts we use in our application. 
This is in pseudo-code. 
They are semantically encoded in the attached ontology.ttl

First we give the essential components of an ontology for a set of votes.
For this we need only two classes and 3 relations. 
    
    Voter votes yes on Bill
    Voter votes no on Bill
    Voter abstains on Bill

It's relevant when a voting event took place

    Bill has date <date>

Features of Voters are interesting, so we collect them. 

    Voter has birthday <birthday>
    Voter has party affiliation Party

To expand for multiple voting sets, we need to distinguish between 
    different VotingAssemblies (parliaments, city councils, etc). 

    Bill is processed by VotingAssembly
    
Interesting meta-data includes the property of VotingAssemblies. 

    VotingAssembly legalizes for Polity

We can refine the meta-data. 

    Polity has subclasses State, Commune, ...

### External Vocabularies and Ontologies

#### Reused Semantic Data

We use dbpedia for uris of political parties and state actors, 
such as `dbr:United_States_Congress`
and `dbr:Democratic_Party_(United_States)>`. 

We also use dbpedia for date of birth (foaf has only age and birthday without year):

    `dbp:birthDate`

#### Constructed Semantic Data

Essential to our application is the combination of different data sources. 
We construct large amounts of data fitting our ontology by querying theirs. 
Currently we have data from http://www.govtrack.us/api/v2 . 
We intend to gather data from at least one other source as well 
    within the scope of this coursework.

## Inferencing

// 100-500 words

// Describe the inferences

*We are currently having technical issues with the actual process of inferencing. 
This section outlines what we want to infer*

### Initial Trivial Inferences

These inferences are trivial but enrich our dataset,
    helping us construct human-friendly dataviews
    as well as providing us useful variables we can reference 
    when computing statistics later on. 

    x votes * on y -> ( x is a Voter , y is a Bill )
    y is processed by z -> ( y is a Bill , z is a VotingAssembly ) 
    ( x votes * on y , y is processed by z ) -> ( x is a Voter , y is a Bill , z is a VotingAssembly, x votes in z )
    x is member of p -> (x is a Voter , p is a Party )

### Voter Age Issue

Voters have a birthday and VoteEvents have a date. 

## Appendix

### Ontology

// Provide the ontology as a separate Turtle file.

### Evidence of Inference

// The ontology should produce meaningful inferences that are essential for the application. This should be evidenced by a screenshot of e.g. Protege reasoning results. (NB: For the final report: inferences should be on the external data)

### Revised version of Milestone 1

// Combine this with a revised version of milestone 1
