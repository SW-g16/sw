
# Domain Modelling
*Semantic Web Course 2016*

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

## Domain and Scope

// 185 / 100-200 words

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

// 101 / 100-200 words

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

// 293 / 200-300 words

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

// 224 / 200-300 words

The four most important classes, around which the ontology is built, are Voter, Voting Assembly, Polity and Bill. All but the latter are subclasses of Actor, as they can be considered to be capable of taking action.

The Voter is a member of a voting assembly, his primary job is to vote on Bills. He can vote either yay or nay on a bill, or abstain from voting, with each of these tree being expressed by a different object property. Voter has a subclass called HumanVoter. This was included in anticipation of integrating EU votes into our ontology, as in that case you have countries voting. Human Voters have an age, a birth date and a gender properties, each of which has an appropriate data property. Depending on these, they are put in subclasses Young Voter, Old Voter, Middle-Aged Voter, Male Voter and/or Female Voter.

A bill is processed by a voting assembly on a certain date. It of course has a text, which is its own data property. A bill applies to a specific polity.

A voting assembly is that in which Bills are introduced and Voters vote for bills. It legalizes for a specific Polity.

A Polity is that to which Bills are applied. It can be put into several subclasses, , which fit different scopes, organizational types and legislative statuses.


## Inferencing

// 106 / 100-500 words

// Describe the inferences

### Initial Trivial Inferences

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
    /know about a dataset containing this information for our Voters. 

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

// Provide the ontology as a separate Turtle file.

### Evidence of Inference

// The ontology should produce meaningful inferences that are essential for the application. 
// This should be evidenced by a screenshot of e.g. Protege reasoning results.
// (NB: For the final report: inferences should be on the external data)

In this screenshot we see data about a Voter and a Bill it supports. 
All Class memberships are inferred. 
![](images/inference_ld-r.png)

### Code Base

For access to our code, we can add you as collaborators in our private GitHub repository upon request. 
Unfortunately there is no option to share a private repository with read-only access
without having to pay. 

### Revised version of Milestone 1

// Combine this with a revised version of milestone 1
