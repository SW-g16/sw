<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Domain Modelling](#domain-modelling)
  - [Domain and Scope](#domain-and-scope)
    - [Required Domain Knowledge](#required-domain-knowledge)
      - [Election and Polling Data](#election-and-polling-data)
  - [Ontology Construction Methodology](#ontology-construction-methodology)
  - [Conceptualization](#conceptualization)
    - [External Vocabularies and Ontologies](#external-vocabularies-and-ontologies)
      - [Reused Semantic Data](#reused-semantic-data)
      - [Constructed Semantic Data](#constructed-semantic-data)
  - [Ontology](#ontology)
  - [Inferencing](#inferencing)
    - [Initial Trivial Inferences](#initial-trivial-inferences)
    - [Voter Age Issue](#voter-age-issue)
  - [Appendix](#appendix)
    - [Ontology](#ontology-1)
    - [Evidence of Inference](#evidence-of-inference)
    - [Revised version of Milestone 1](#revised-version-of-milestone-1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

/*
    this is a stub for tomorrow's delivery. 
    everything in java-style comments are comments for us, 
    everything else is part of the doc as we deliver it
*/

# Domain Modelling
*Semantic Web Course 2016*

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

## Domain and Scope

// 100-200 words

// Description of the domain and scope of the ontology, as determined by the application 

// what's the difference between domain and scope?

Our domain consists of the voting data of a number of legislative assemblies, 
each belonging to a different political entity. For this voting data, we map 
which bills were voted on, those who vote for these bills and how they voted, 
and the composition of the legislative assembly over time. The relevant data is 
drawn from the data made available by the political entities in question, which 
is then fused into a single, combined ontology. This ontology was designed for 
those with an interest in the political process, allowing them to look up voting 
history and patterns. 
    
### Required Domain Knowledge

To understand the domain in question, all that is required is a basic 
understanding of voting processes and institutions: Assembly members vote for 
bills in assemblies, with the bills that attain a sufficient percentage of votes 
then being applied to the relevant polity.

#### Election and Polling Data

A promising expansion of our ontology would be to combine it with election 
results and inter-election polls. This would allow for mapping how closely 
assembly voting matches the desires of the populace at a given point in time.

## Ontology Construction Methodology

// 100-200 words

// Description of the methodology that is used in the construction of the ontology 

// methodology? we opened protege, then clicked stuff until we were done

As outlined under 'Domain and Scope' (and detailed in 'Conceptualization'), our 
goal was to create an ontology that allows a user to look up voting history and 
patterns for a variety of voting assemblies. For this, we first needed to 
investigate which legislative assemblies had the relevant data publicly 
available in a manner that could automatically be extracted. Next, we needed to 
see what additional data was available for the legislative assembly members, and 
which of that data would be relevant to looking up voting patterns. Finally, the 
practical task of ontology construction was done in the Protégé ontology editor.



## Conceptualization

// 200-300 words

// Conceptualization of the domain (concepts, relations) described, discussed and depicted in a drawing. 
// The conceptualization should encompass more than 15 classes and at least 5 properties 

// todo insert screenshot of ontog

First, we need the essential components for describing a set of non-anonymous 
votes. For this, we only need two classes and three relations.

    Voter votes yes on Bill
    Voter votes no on Bill
    Voter abstains on Bill

The date of a voting event is a relevant piece of data, so an additional 
relation is created to describe that.

    Bill has date <date>

Voters have several interesting features, which are also collected.

    Voter has birthday <birthday>
    Voter has party affiliation Party

Voters are further categorized to allow identification of potential voting 
patterns.
					
    Voter has subclasses MiddleAgedVoter, YoungVoter, OldVoter, FemaleVoter, MaleVoter

To expand the ontology to encompass multiple legislative assemblies, an 
additional relation is needed to distinguish between them.

    Bill is processed by VotingAssembly

For each legislative assembly, there is the relevant data of what polity it 
legislates for.

    VotingAssembly legalizes for Polity

Polities can be divided into several subcategories, describing different scopes, 
organizational types and legislatives statuses. 

    Polity has subclasses State, Commune, Federation, County

### External Vocabularies and Ontologies

#### Reused Semantic Data

DBpedia is used for the URIs of political parties and state actors, such as 
`dbr:United_States_Congress` and `dbr:Democratic_Party_(United_States)>`. 
DBpedia is also used for date of birth (`dbp:birthDate`), as foaf only has age 
and date of birth, not specifying the year.

#### Constructed Semantic Data

Combination of a variety of data sources is essential to our application. Large 
quantities of data fitting our ontology are constructed by querying the publicly 
available data of political entities. Currently, data for our ontology is drawn 
from the United States government at http://www.govtrack.us/api/v2, but there 
are plans to gather data from at least one additional source during the scope of 
this coursework as well. Currently, the data of the European Council is being 
considered.

## Ontology

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

// The ontology should produce meaningful inferences that are essential for the application. 
// This should be evidenced by a screenshot of e.g. Protege reasoning results.
// (NB: For the final report: inferences should be on the external data)

### Revised version of Milestone 1

// Combine this with a revised version of milestone 1
