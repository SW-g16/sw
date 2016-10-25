<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Final Report](#final-report)
  - [Table of Contents](#table-of-contents)
  - [Abstract](#abstract)
  - [Introduction](#introduction)
  - [Application Design (Milestone 1)](#application-design-milestone-1)
    - [Goals](#goals)
      - [Primary Goals](#primary-goals)
      - [Secondary Goals](#secondary-goals)
    - [Users](#users)
      - [Satistfaction Requirements](#satistfaction-requirements)
        - [TG_1: People with domain interest](#tg_1-people-with-domain-interest)
        - [TG_2: Developers](#tg_2-developers)
        - [TG_3: People who are attracted to data visualizations](#tg_3-people-who-are-attracted-to-data-visualizations)
      - [Satisfaction Requirements per Target Group](#satisfaction-requirements-per-target-group)
        - [Implied Technical Requirements (TRs)](#implied-technical-requirements-trs)
    - [Design](#design)
      - [The LD-R Framework](#the-ld-r-framework)
        - [Code Location / Method](#code-location--method)
        - [Network Graph Browser](#network-graph-browser)
        - [Text-based Browser](#text-based-browser)
      - [Devices](#devices)
      - [Possible Extensions](#possible-extensions)
    - [Walkthrough](#walkthrough)
  - [Domain Modeling (Milestone 2)](#domain-modeling-milestone-2)
    - [Domain and Scope](#domain-and-scope)
      - [Domain](#domain)
        - [Required Domain Knowledge](#required-domain-knowledge)
      - [Scope](#scope)
      - [Mapping and Inferencing Between Political entities](#mapping-and-inferencing-between-political-entities)
        - [Election and Polling Data](#election-and-polling-data)
    - [Ontology Construction Methodology](#ontology-construction-methodology)
      - [Vocabulary Definition Process](#vocabulary-definition-process)
      - [Automatic Data Querying and Construction](#automatic-data-querying-and-construction)
        - [Identifying Candidate Sources](#identifying-candidate-sources)
        - [Evaluating and Accessing Candidate Sources](#evaluating-and-accessing-candidate-sources)
        - [Coding Custom Querier and Data Constructor](#coding-custom-querier-and-data-constructor)
          - [Issues with Current Implementation](#issues-with-current-implementation)
    - [Conceptualization](#conceptualization)
      - [External Vocabularies and Ontologies](#external-vocabularies-and-ontologies)
        - [Reused Semantic Data](#reused-semantic-data)
        - [Constructed Semantic Data](#constructed-semantic-data)
    - [Ontology](#ontology)
    - [Inferencing](#inferencing)
      - [Initial Trivial Inferences](#initial-trivial-inferences)
      - [Less Trivial Inferences](#less-trivial-inferences)
- [Appendix](#appendix)
  - [Ontology](#ontology-1)
  - [Evidence of Inference](#evidence-of-inference)
  - [Code Base](#code-base)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# Final Report

*Semantic Web Course 2016*

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

*[latest version of this document on GitHub](https://github.com/SW-g16/sw/blob/master/documentation/final-report.md).*

## Table of Contents

- [Final Report](#final-report)
  - [Table of Contents](#table-of-contents)
  - [Abstract](#abstract)
  - [Introduction](#introduction)
  - [Application Design (Milestone 1)](#application-design-milestone-1)
    - [Goals](#goals)
      - [Primary Goals](#primary-goals)
      - [Secondary Goals](#secondary-goals)
    - [Users](#users)
      - [Satistfaction Requirements](#satistfaction-requirements)
        - [TG_1: People with domain interest](#tg_1-people-with-domain-interest)
        - [TG_2: Developers](#tg_2-developers)
        - [TG_3: People who are attracted to data visualizations](#tg_3-people-who-are-attracted-to-data-visualizations)
      - [Satisfaction Requirements per Target Group](#satisfaction-requirements-per-target-group)
        - [Implied Technical Requirements (TRs)](#implied-technical-requirements-trs)
    - [Design](#design)
      - [The LD-R Framework](#the-ld-r-framework)
        - [Code Location / Method](#code-location--method)
        - [Network Graph Browser](#network-graph-browser)
        - [Text-based Browser](#text-based-browser)
      - [Devices](#devices)
      - [Possible Extensions](#possible-extensions)
    - [Walkthrough](#walkthrough)
  - [Domain Modeling (Milestone 2)](#domain-modeling-milestone-2)
    - [Domain and Scope](#domain-and-scope)
      - [Domain](#domain)
        - [Required Domain Knowledge](#required-domain-knowledge)
      - [Scope](#scope)
      - [Mapping and Inferencing Between Political entities](#mapping-and-inferencing-between-political-entities)
        - [Election and Polling Data](#election-and-polling-data)
    - [Ontology Construction Methodology](#ontology-construction-methodology)
      - [Vocabulary Definition Process](#vocabulary-definition-process)
      - [Automatic Data Querying and Construction](#automatic-data-querying-and-construction)
        - [Identifying Candidate Sources](#identifying-candidate-sources)
        - [Evaluating and Accessing Candidate Sources](#evaluating-and-accessing-candidate-sources)
        - [Coding Custom Querier and Data Constructor](#coding-custom-querier-and-data-constructor)
          - [Issues with Current Implementation](#issues-with-current-implementation)
    - [Conceptualization](#conceptualization)
      - [External Vocabularies and Ontologies](#external-vocabularies-and-ontologies)
        - [Reused Semantic Data](#reused-semantic-data)
        - [Constructed Semantic Data](#constructed-semantic-data)
    - [Ontology](#ontology)
    - [Inferencing](#inferencing)
      - [Initial Trivial Inferences](#initial-trivial-inferences)
      - [Less Trivial Inferences](#less-trivial-inferences)
- [Appendix](#appendix)
  - [Ontology](#ontology-1)
  - [Evidence of Inference](#evidence-of-inference)
  - [Code Base](#code-base)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Abstract

## Introduction

## Application Design (Milestone 1)

### Goals

#### Primary Goals

 - Provide an endpoint combining open voting data from different sources
 - Achieve 5 timbl-stars
 - Define meaningful Data Views for humans
 - Output data views to LD-R UI components

#### Secondary Goals

 - Integrate a visual network graph data browser as a LD-R UI component, or apply one if such a component already exists
 - Analyze the data using machine learning techniques for semantic data
 - Define Data Views for viewing statistics / interesting output of analyzing machine
 - Visualize statistics / analyzer output with standard plots and charts within a LD-R UI component.

### Users

#### Satistfaction Requirements

We identify some satisfaction requirements that some user may have.

 - **Facts**: Who voted for what? What passed and what failed, and with what margin?
 - **Analysis**: What patterns exist in the behavior of voters, parties and voting assembles? How do entities cluster and how do values correlate?
 - **Shareability**: possibility of sharing views with others
 - **visualization**: visualizations make structures in data easier
 - **Documentation**: We thoroughly document our app's functionality.
 - **Code accessibility**: We make our code readable and available under an open license on GitHub

We define some Target Groups.


##### TG_1: People with domain interest

These users are interested in the data itself, and in any patterns that can be seen in it.
They view visualizations as tools to understand the data, and are unlikely to care about the machine's inner workings.

##### TG_2: Developers

These take an interest in how our application works and might want to view or use our code.
They inherit the needs of all other users.

##### TG_3: People who are attracted to data visualizations

This group may skip past explanatory text to look at visualizations, regardless of the domain.
This group wants to understand as much information as efficiently as possible from data visualizations.

#### Satisfaction Requirements per Target Group

The TGs have these SRs, in no particular order.

|Target Group|Fact|Analysis|Sharability|Visualization|Documentation|Code Accessibility|
|---|---|---|---|---|---|---|
|TG_1|1|1|1|1|0|0|
|TG_2|1|1|1|1|1|1|
|TG_3|0|1|1|1|0|0|

##### Implied Technical Requirements (TRs)

The SRs imply these TRs, in no particular order.

|TR_id|is essential|description|
|---|---|---|
|TR_0|yes|Combine a set of data sources into a single ontology|
|TR_1|yes|Present semantic data to users through custom Data Views|
|TR_2|yes|Perform some inference|
|TR_4|no|Compute and present trivial statistics to users through custom Data Views|
|TR_5|no|Visualize trivial statistics|
|TR_6|no|Perform non-trivial analysis on voting data to |
|TR_7|no|Visualize results of non-trivial analysis|

### Design

#### The LD-R Framework

We use the LD-R framework to avoid reinventing wheels.
Web pages are generated for us, after we apply our custom configurations.

##### Code Location / Method

We design our interface by modifying config files of LD-R.

##### Network Graph Browser

We may integrate some semantic network graph browser as an LD-R component.
[WebVOWL](http://vowl.visualdataweb.org/webvowl/index.html) seems relevant.

##### Text-based Browser

We create Data Views that generate tabular and object 'profile pages'.

#### Devices

Our application inherits the mobile-first layout of LD-R.
However for some visualizations it is sometimes desirable to have a larger screen,
as it allows for communicating more information at once.

#### Possible Extensions

We may consider adding our own API functionality through a SPARQL endpoint,
allowing technical users to work with our data in their own applications.
Finally, the project will all be open source,
allowing anyone to understand and expand on our code-base.

### Walkthrough

A user lands on the main page and is presented with an overview of the data.
The user clicks a link to an entity and sees all relevant data (defined by a Data View) associated with it,
    including inferred statements.
There is also a set of graphs and statistics available.
The user finds these interesting, and copies the URL currently in the address bar and posts to their friend.
 the friend sees the same data in the same way as the first user, and they both like the link on Facebook.

The user wants to generate a graph of data defined by applying user-defined filters on the dataset.
The user sets their filters.
The filters include restrictions like only showing bills from a specific period, only showing people that voted a specific way on a specific bill,
     only showing politicians that fit a particular profile (such as wealth, level of education, nation of birth or gender),
The user hits submit.
Upon a warning, the user realizes they were about to init getting and rendering of a very large amount of data and hit cancel.
They modify their filter and retries.
A semantic graph is returned, and sent to our WebVowl component for visualization.

## Domain Modeling (Milestone 2)

### Domain and Scope

#### Domain

Our domain is the set of Voting Assemblies' Voters votes on Bills around the world,
    and other immediately relevant and interesting data.
Our data is imported from the political entities in question, and
 is then fused into a single, combined ontology.
Assertions we are interested include
 - Who votes for what?
 - What features does each Voter have? Income? Education? Board Memberships? ASL?
For inferring results of votes:
 - What is the threshold for a bill to pass?
For the relationships between and among Polities, Bills, and Voting Assemblies,
 - Which Polities inherit Bills of which other Polities?
 - Which Voting Assemblies pass Bills onto which Polit(y/ies)?

##### Required Domain Knowledge

To understand the domain in question, all that is required is a basic
understanding of voting processes and institutions: Assembly members vote for
bills in assemblies, with the bills that attain a sufficient percentage of votes
then being applied to the relevant polity.

#### Scope

Due to the quantity and variety of data available on various political entities, the potential of this project is vast.
For that reason, we are currently limiting our ontology to the data of a single political entity (The US Government).
Mapping it to geographic and demographic information about politicians.
The majority of mapping and inferencing will be based on the backgrounds of the politicians and their parties.

#### Mapping and Inferencing Between Political entities
If our ontology proves to be robust, we will expand our mapping to be between multiple political entities, creating a higher level of inferencing by comparing the entities themselves.

##### Election and Polling Data

Another promising expansion of our ontology would be to combine it with election results and inter-election polls.
This would allow for mapping how closely assembly voting matches the desires of the populace at a given point in time.

### Ontology Construction Methodology

#### Vocabulary Definition Process

Our vocabulary is designed to express voting data and some other related data from a number of different sources.
Its construction was enabled by a basic level of domain knowledge.
The practical task of ontology construction was done in the Protégé ontology editor.

#### Automatic Data Querying and Construction

We acquire large amounts of data and map it to our vocabulary,
    before inserting it into our semantic database.

The process of acquiring this data consists of

 1. identifying candidate sources
 2. evaluating and accessing candidate
 3. coding custom queriers and data constructors for different data sources

##### Identifying Candidate Sources

One of the first steps in our Agile development approach, was to do in-depth research into the the open data provided by governments and political bodies. This research helped us with many of our design choices. After identifying many possibilities, we narrowed our choices (based on the quality and depth of data) to the following:
  - [US Governmental data (GovTrack)](https://www.govtrack.us/)
  - [UK Parliament bill progress tracking](http://www.data.parliament.uk/dataset/bills)
  - [European Council votes on legislative acts](http://data.consilium.europa.eu/)

##### Evaluating and Accessing Candidate Sources

|Provider name|endpoint|timblr-stars|comment|
|---|---|---|---|
|GovTrack|http://www.govtrack.us/api/v2/|3|Data encoded in custom JSON format|
|UK Parliament|http://lda.data.parliament.uk/bills.json|3|Data encoded in custom JSON/XML/CSV formats|
|European Council|http://data.consilium.europa.eu/sparql|4|Data available through SPARQL endpoint, but is not linked to any external data|

##### Coding Custom Querier and Data Constructor

So far we've programmed one Data Getter.
It is written in Python and works by querying govtrack.us,
    translating JSON data in Govtrack's format to semantic triples
    before inserting the the triples to our database.

###### Issues with Current Implementation

There are some issues with.

 - We're converting from a custom JSON data to a custom TTL vocabulary in Python,
    without using helpful libraries where we could.
 - We're doing many small queries instead of one large bulk download of the source data.
    This should change out of respect to the data provider and for efficiency of the import task.

### Conceptualization

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

#### External Vocabularies and Ontologies

##### Reused Semantic Data

DBpedia is used for the URIs of political parties and state actors, such as
`dbr:United_States_Congress` and `dbr:Democratic_Party_(United_States)>`.
DBpedia is also used for date of birth (`dbp:birthDate`), as foaf only has age
and date of birth, not specifying the year.

##### Constructed Semantic Data

Combination of a variety of data sources is essential to our application. Large
quantities of data fitting our ontology are constructed by querying the publicly
available data of political entities. Currently, data for our ontology is drawn
exclusively from GovTrack, but the possibility to combine with more sources remains open.
We intend to gather data from at least one additional source within the scope of
this coursework as well.

### Ontology
The four most important classes, around which the ontology is built,
    are Voter, Voting Assembly, Polity and Bill.
All but the latter are subclasses of Actor, as they can be considered to be capable of taking action.
The Voter is a member of a voting assembly, his primary job is to vote on Bills.
They can vote either "yay" or "nay" on a bill, or abstain from voting,
    with each of these tree being expressed by a different object property.
Voter has a subclass HumanVoter, defined in anticipation of integrating EU votes into our ontology,
    where the Voters are not HumanVoters but Countries.

Human Voters have an age, a birth date and a gender property,
    each of which has an appropriate data property.
Depending on these, they are put in subclasses Young Voter, Old Voter, Middle-Aged Voter, Male Voter and/or Female Voter,
    inferred from the rules we use assert in our ontology.

A bill is processed by a voting assembly on a certain date.
It of course has a text, which is its own data property.
A bill applies to a specific polity.

A voting assembly is that in which Bills are introduced and Voters vote for bills.
It legalizes for a specific Polity.

A Polity is that to which Bills are applied.
It can be put into several subclasses, which fit different scopes, organizational types and legislative statuses.


### Inferencing

#### Initial Trivial Inferences

*In this section, we use a pseudo-formal ad-hoc notation to communicate
    steps we want to either infer or deduce.*

These inferences are trivial but enrich our dataset,
    helping us construct human-friendly data-views
    as well as providing us useful variables we can reference
    when computing statistics later on.

    x votes * on y -> ( x is a Voter , y is a Bill )
    y is processed by z -> ( y is a Bill , z is a VotingAssembly )
    ( x votes * on y , y is processed by z ) -> ( x is a Voter , y is a Bill , z is a VotingAssembly, x votes in z )
    x is member of p -> (x is a Voter , p is a Party )

Another trivial inference is that a Voter belongs to a certain income class (x%-buckets).
While the inference is trivial, we don't currently have access to

    ( Voter x income 291432 , UpperClassVoter is equivalent to ( Voter, numberOfResults(select voter v1 where v1.income > x.income)<num_voters/3*2 ) )

#### Less Trivial Inferences

The following Inferences involve arithmetics and gives interesting data which we can compute statistics from.
We have not yet enabled these inferences, but we intend to.

    # a voter's age upon a voting event
    ( x votes * on y , y has date date_1, x has birthdate date_2 ) -> Voter had age (date_1-date_2) at time of vote

    # from age we can infer age groups
    ( x has age < 40 ) -> x is a YoungVoter

    # ... more bucket categories can be made for other voter features

    # a Party is a DominantParty if it has the majority of Voters
    ( Party p has x voters , x/number of voters > 0.5 ) -> p is a DominantParty

    # Proportion of yay vs nay
    ( bill b has x yayvotes, bill b has y nayvotes ) -> yayproportion = x/y

    # result computation
    # NB: yayproportion required for a Bill to pass may vary between voting assemblies
    ( bill has yayproporion >=0.5 ) -> b passed
    ( bill has yayproporion <0.5 ) -> b failed


## Data Reuse and Querying (Milestone 3)


    /*
        1. (100-200 words) a description of at least 2 external sources of data that will be used by your application. At least one of these must be an external SPARQL endpoint. The other dataset need not be in RDF. 
        2. (100-200 words) a motivation for choosing these data sources: why does the application need these sources specifically. 
        3. (200-300 words) a description of how you produce integrated the data with your ontology, did you use inferencing? 
        4. (100-200 words) a description of multiple complex SPARQL queries, relevant for the application, that produce results over the integrated data and ontology 
        5. (200-300 words) a description and evidence that running the SPARQL queries against the ontology and data produces inferences (screenshot reasoning on/off). Discuss the inferences. 
    */

We're interested in 


 - any data about individual voters 
 - text, date, and votes on a bill
 - which voting assembly has which voters and bills

> In a September 2011 joint report from the National Democratic Institute and World Bank Institute, a survey of parliamentary monitoring organisations (PMOs) found that parliamentary informatics are used by approximately 40 percent of PMOs worldwide. " - wikipedia.org/wiki/Parliamentary_informatics) 

So there's lots of data available. If we were to continue this project beyond the scope of this course, we'd want to mine every available source. For now we retrieve data from govtrack, parltrack and dbpedia. 

### Data Sources

#### GovTrack

From govtrack's data, we mine voter ids, some voter info, bills, and votes. 
See the govtrack data getter code for comments on it's structure. 

#### ParlTrack


### Motivation for using these sources 
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

### Description how you integrated the data (200-300 words)
In our ontology, we speak of four classes as being central: Voters, Bills, 
Assembly and Polity. Voter and Bills are found in the contents of the datasets
we mined. Assembly and Polity are determined by which dataset the data comes
from. 


### Querying and Data Analysis 

We now have lots of data which we can analyze by sending complex sparql queries to our database. 
There's no limit to the number of different analyses we can do / queries we can write. 
Below we give some low-hanging ones. 

#### Voting Assembly Party Compositions

The following query returns the proportion of parties' representation in a voting assembly at the time of a certain bill. Since we have a unified ontology, this will of course work for any of our 2 data sources. Inference is involved: we never explictly store that a resource is a Voter, it is inferred from the fact that they vote, because `:votesOn rdfs:Domain :Voter`. 
  
  select ?voting_assembly ?date ?party where {complex condition}

##### Another complex query relying on inferencing

This is a description of the query. 

  select ?stuff where {complex condition}
  
# Appendix

## Ontology

Find [our ontology at GitHub](http://www.github.com/SW-g16/ontology)

## Evidence of Inference

In this screenshot we see data about a Voter and a Bill it supports.
All Class memberships are inferred. 
![](images/inference_ld-r.png)

## Code Base

Find [our code at GitHub](http://www.github.com/SW-g16)
