
# Domain Modelling
*Semantic Web Course 2016*

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

## Domain and Scope

### Domain

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

#### Required Domain Knowledge

To understand the domain in question, all that is required is a basic
understanding of voting processes and institutions: Assembly members vote for
bills in assemblies, with the bills that attain a sufficient percentage of votes
then being applied to the relevant polity.

### Scope

Due to the quantity and variety of data available on various political entities, the potential of this project is vast. 
For that reason, we are currently limiting our ontology to the data of a single political entity (The US Government). 
Mapping it to geographic and demographic information about politicians. 
The majority of mapping and inferencing will be based on the backgrounds of the politicians and their parties.

#### Mapping and Inferencing Between Political entities
If our ontology proves to be robust, 
    we will expand our mapping to be between multiple political entities, 
    creating a higher level of inferencing by comparing the entities themselves.

#### Election and Polling Data

Another promising expansion of our ontology would be to combine it with election results and inter-election polls. 
This would allow for mapping how closely assembly voting matches the desires of the populace at a given point in time.

## Ontology Construction Methodology

### Vocabulary Definition Process

Our vocabulary is designed to express voting data and some other related data from a number of different sources.
Its construction was enabled by a basic level of domain knowledge.
The practical task of ontology construction was done in the Protégé ontology editor.

### Automatic Data Querying and Construction

We acquire large amounts of data and map it to our vocabulary,
    before inserting it into our semantic database.

The process of acquiring this data consists of

 1. identifying candidate sources
 2. evaluating and accessing candidate
 3. coding custom queriers and data constructors for different data sources

#### Identifying Candidate Sources

By Googlin around we find a list of sources, detailed in the table of the next section. 

#### Evaluating and Accessing Candidate Sources

|Provider name|endpoint|timblr-stars|comment|
|---|---|---|---|
|GovTrack|http://www.govtrack.us/api/v2/|3|data encoded in their own custom json format|

#### Coding Custom Querier and Data Constructor

So far we've programmed one Data Getter. 
It is written in Python and works by querying govtrack.us, 
    translating json data in govtrack's format to semantic triples
    before inserting the the triples to our database. 

##### Issues with Current Implementation

There are some issues with. 

 - We're converting from a custom json-data to a custom ttl vocabulary in Python, 
    without using helpful libraries where we could. 
 - We're doing many small queries instead of one large bulk download of the source data. 
    This should change out of respect to the data provider and for efficiency of the import task.

## Conceptualization

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
exclusively from GovTrack, but the possibility to combine with more sources remains open. 
We intend to gather data from at least one additional source within the scope of
this coursework as well. 

## Ontology
The four most important classes, around which the ontology is built, 
    are Voter, Voting Assembly, Polity and Bill. 
All but the latter are subclasses of Actor, 
    as they can be considered to be capable of taking action.
The Voter is a member of a voting assembly, his primary job is to vote on Bills. 
They can vote either yay or nay on a bill, or abstain from voting, 
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


## Inferencing

### Initial Trivial Inferences

*In this section, we use a pseudo-formal ad-hoc notation to communicate 
    steps we want to either infer or deduce.*

These inferences are trivial but enrich our dataset,
    helping us construct human-friendly dataviews
    as well as providing us useful variables we can reference
    when computing statistics later on.

    x votes * on y -> ( x is a Voter , y is a Bill )
    y is processed by z -> ( y is a Bill , z is a VotingAssembly )
    ( x votes * on y , y is processed by z ) -> ( x is a Voter , y is a Bill , z is a VotingAssembly, x votes in z )
    x is member of p -> (x is a Voter , p is a Party )

Another trivial inference is that a Voter belongs to a certain income class (x%-buckets).
While the inference is trivial, we don't currently have access to

    ( Voter x income 291432 , UpperClassVoter is equivalent to ( Voter, numberOfResults(select voter v1 where v1.income > x.income)<num_voters/3*2 ) )

### Less Trivial Inferences

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


## Appendix

### Ontology


### Evidence of Inference

In this screenshot we see data about a Voter and a Bill it supports.
All Class memberships are inferred.
![](images/inference_ld-r.png)

### Code Base

For access to our code, we can add you as collaborators in our private GitHub repository upon request.
Unfortunately there is no option to share a private repository with read-only access
without having to pay.

