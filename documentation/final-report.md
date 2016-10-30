
# Final Report

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

*For the Semantic Web Course at VU Amsterdam, 2016*

*Keywords: semantic web, data mining, sparql querying, inferencing parliamentary informatics, government data, open data* 

*[latest version of this document on GitHub](https://github.com/SW-g16/sw/blob/master/documentation/final-report.md).*

*screenshots are taken on a small test dataset*

## Abstract

> In a September 2011 joint report from the National Democratic Institute and World Bank Institute, a survey of parliamentary monitoring organisations (PMOs) found that parliamentary informatics are used by approximately 40 percent of PMOs worldwide. " - wikipedia.org/wiki/Parliamentary_informatics) 

An increasing amount of data on elected representative's votes on bills are being made freely available online, but they do not share a common format.
This report documents a framework and several instance components for combining these sources into a single ontology, 
making it easier to perform data analysis across the data of several different voting assemblies. 
The system integrates data miners, UIs, and a semantic database, 
forming a functioning system ready to be expanded to include more data sources, more sophisticated data analysis, 
and more intuition-friendly ways of visualizing the data and analysis results. 

## Introduction
This report was made for the course 'Semanatic Web', at the Vrije Universiteit of Amsterdam, in which students were tasked with creating a semantic web application of their own choice. For this task, our group chose to tackle politics. We had learned that many legislative assemblies have been making parliamentary informatics available, but we could find no tool that allowed for analysis and oversight of such parliamentary informatics. As such, we decided to make one of our own. Specifically, we decided to create a modular tool for visualizing and filtering the voting-related data from a small set of legislative assemblies.
ctrl+z? 
This report covers the creation of that tool.

This report is structured according to the milestones set for the course. In the first milestone we will talk about planning the application design, establishing the goals, 
identifying the potential users, determining how we are going to design it, and giving a short walkthrough of how it will work. In the second milestone, we will talk about the ontology for our application, explaining the planned domain and scope, how the ontology was conceptualized and constructed, provide a short description and describe how the ontology will infer new information. Finally, in the third section, we will describe the more practical parts of our application, such as where it gets the data from, how it integrates said data and how it is queried. In the end, we talk about project conclusions, and the possibilities for future developments.

## Goals

The goal of this project was to provide an application capable of mining, analyzing, and presenting data on votes, voters and bills of legislative assemblies, providing users with some oversight and tools to consume this data. To achieve this, the following sub-goals have been established:

 - The provision of an endpoint that combines the open voting data from a number of legislative assemblies.
 - The enrichment of this endpoint, to reach 5-TimBL stars.
 - Using the data to infer further triples.
 - Definition of meaningful Data Views for this endpoint.
 - The provision of a human-friendly interface that applies these Data Views.

## Application 
### Description
#### Open Endpoint
Upon application deployment, a read-only SPARQL endpoint would be made publicly available, releasing the project data to the semantic web.

#### Technical Requirements
The goals and project requirements imply the following Technical Requirements

|TR_id|is essential|description|
|---|---|---|
|TR_0|yes|Combine a set of data sources into a single ontology|
|TR_1|yes|Present semantic data to users through custom Data Views|
|TR_2|yes|Perform some inference|
|TR_4|no|Compute and present trivial statistics to users through custom Data Views|
|TR_5|no|Visualize trivial statistics|
|TR_6|no|Perform non-trivial analysis on voting data to |
|TR_7|no|Visualize results of non-trivial analysis|

*Table 1: Technical requirements and their level of essentiality*

## Users
### Satisfaction Requirements
For description of the application's target groups, the following satisfaction requirements were defined

 - **Facts**: The ability of the program to provide the users with certain facts. Who voted for what? What passed and what failed, and with what margin?
 - **Analysis**: The ability of the program to allow the user to analyze the data. What patterns exist in the behavior of voters, parties and voting assembles? How do entities cluster and how do values correlate?
 - **Shareability**: The ability of the program to allow one user to share his current view of the data with other users.
 - **Visualization**: The ability of the program to visualise the data in a clear and concise way.
 - **Documentation**: The degree to which the program is documented, and the documentation is clear.
 - **Code accessibility**: The degree to which our code is open and accessible. 

### Target groups by Satistfaction Requirements

|Target Group|Fact|Analysis|Sharability|Visualization|Documentation|Code Accessibility|
|---|---|---|---|---|---|---|
|TG_1|1|1|1|1|0|0|
|TG_2|1|1|1|1|1|1|
|TG_3|0|1|1|1|0|0|

*Table 2: Target Groups and projected satisfaction requirements*

#### Target group 1: People with domain interest
These users are interested in the data itself, and in any patterns that can be found in said data.
They view visualizations as tools to understand the data, and are unlikely to care about the machine's inner workings.

#### Target group 2: Developers
These users take an interest in how our application works and might want to view or use our code.
They inherit the needs of all other users.

#### Target group 3: People who are attracted to data visualizations
These users may skip past explanatory text to look at visualizations, regardless of the domain.
They want to understand as much information as efficiently as possible from data visualizations.

## Interface Design
### Walkthrough

Upon initialization, the user is presented with the default page, providing him with an overview of the data, as well as links to acess to acess the data of the various political entities. Clicking one of these will bring up all the relevant data (as defined by a Data View) taken from that source, associated with that source through interlinking of endpoints, or inferred about that source. The user may also click additional buttons for the generation of graphs and statistics. If a user finds this data interesting enough to share, he can do so by copying the URL currently in the address bar, and sharing that URL. Any other user who opens that link will see the same data in the same way as the first use.

Users can also generate a graph of the data defined by applying their own user-defined filters on the dataset. A user may select filters such as only showing bills from a specific period, only showing people that voted a specific way on a specific bill or only showing politicians that fit a particular profile (such as wealth, level of education, nation of birth or gender). Upon selecting these filters, the user presses 'submit'. If the amount of data that is called is sufficiently large, the user is provided with a warning prompt, giving him a chance to cancel, upon which the user can modify their filter and retry. Upon submission, a semantic graph is returned, sent to the application's WebVowl component for visualization.


In this section we describe our interface in terms of what components it consists of, 
what tasks it performs, and how it interacts with other components.

The interface includes the LD-R browser, a highly configureable semantic web browser. 
LD-R is suitable for our application, but unfortunately we did not succeed in configuring it in time for the deadline of this project. 
Instead we are including a fiddle which performs some of the tasks we intended for LD-R (and our intended extentions to it) to do. 

### Data Views

Data views are implictly defined by queries generated from user's uri lookups, implemented through GET requests. 
The data views are varied, and may or may not include statistics on the requested data. 
We've only implemented two views, but have the framework to increase this number indefinitely. 
In both views, the column headers of the screenshot together explicitly define the data view. 

#### Party View

This view gives a summary of a specific party. Note the uri as value of `bill` in the url bar, 
which is dereferenced by the interface. 

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/party.png)

*Image 1: Party View*

#### Parties View

This view gives a summary of a set of parties. It takes no input. 

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/parties.png)

*Image 2: Parties View*

#### Statistics in Data Views

As evidenced in the above screenshots, our data views include statistics. 
These are currently computed on-the-fly, which is unecessary since it will return the same result until the database is updated. 
This would have to change before a potential employment - the current solution is not scalable. 
The results of statistics should be stored, and analysis should be rerun only when new data becomes available. 
The statistics computed are `proportion of abstaining party members`
and ´unity = (number of upvoters - number of downvoters) / (number of upvoters + number of downvoters)´. 

#### Visualization 

As evidenced in the screenshot at [Party View](#Party-View), we perform some basic visualization of the some data. 
Here, we plot the values of the statistics defined above across time. 

### LD-R 

We intended to do everything we're currently doing in the fiddle within LD-R. 
We were bottlenecked by inability to configure data views with it. 
Until we succeed in this, we only use the default configurations of LD-R. 
LD-R is still a useful interface, even without customization,
as it allows us to semantically browse our data and inferences made from it. 
Below is a screenshot of LD-R listing our entities.

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/ldr_list.png)

*image 3: LD-R Screenshot*

### Network Graph Browser

We considered integrating some semantic network graph browser as an LD-R component, 
    such as [WebVOWL](http://vowl.visualdataweb.org/webvowl/index.html).

### Platform

#### Devices
Our application inherits the mobile-first layout of LD-R.
However for some visualizations it is sometimes desirable to have a larger screen,
as it allows for communicating more information at once.

## Domain and Scope

### Domain

The domain of our ontology is the set of Voting Assemblies' Voters' votes on Bills around the world, and other immediately relevant and interesting data related to this. Our data is imported from the political entities in question, and is then fused into a single, combined ontology. 

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
For that reason, we are currently limiting our ontology to the data of but two political entities: The US government, and the European Council.
Extracted data is mapped to geographic and demographic information about politicians.
The majority of mapping and inferencing is based on the backgrounds of the politicians and their parties.

### Mapping and Inferencing Between Political entities
If our ontology proves to be robust, we will expand our mapping to be between multiple political entities, creating a higher level of inferencing by comparing the entities themselves.

#### Election and Polling Data

Another interesting expansion of our ontology would be to combine it with election results and inter-election polls.
This would allow for mapping how closely assembly voting matches the desires of the populace at a given point in time.

## Conceptualization

First, the essential components for describing a set of non-anonymous
votes are needed. For this, only two classes and three relations are needed.

    Voter votes yes on Bill
    Voter votes no on Bill
    Voter abstains on Bill

To expand the ontology to encompass multiple legislative assemblies, an
additional relation is needed to distinguish between them.

    Bill is processed by VotingAssembly

The above are the 4 fundamental triples that make up the backbone of the application's graph. 
Data collected beyond is only appended to the graph. 
The appended data serves to *enrich* the application's ontology, 
both in the semantic sense (referencing external resources), 
and in the sense that it enables more interesting analyses on the data. 

A bill's date is relevant. 

    Bill has date <date>

Voters have several interesting features, which are also collected.

    Voter has birthday <birthday>
    Voter has party affiliation Party

Voters are further categorized to allow identification of potential voting
patterns.

    Voter has subclasses MiddleAgedVoter, YoungVoter, OldVoter, FemaleVoter, MaleVoter

For each legislative assembly, there is the relevant data of what authority it processes votes for, and to which polity the authority applies the passed votes to. 

    VotingAssembly processes votes for Authority

    Authority legalizes for Polity


Polities can be divided into several subcategories, describing different scopes,
organizational types and legislatives statuses.

    Polity has subclasses State, Commune, Federation, County

 There is room for a lot of further refinement in many directions as we move further away from our core structure, 
 which is the sets of `Voter direction Votable` and `Votable processedBy VotingAssembly` triples 
    
## Ontology 

### Vocabulary 

Our vocabulary is designed to express voting data and other related data from a variety of sources.
Its construction was enabled by a basic level of domain knowledge and an intermediate understanding of OWL.
The practical task of ontology construction was performed using the Protege ontology editor.

### Ontology Construction

A vocabulary becomes an ontology when instance data is added to it. 
The combined ontology includes a custom vocabulary and instance data mined from external sources. 
In addition to using the custom vocabulary, the instance data also includes references to external sources. 
These resources include both central properties like `dbo:party` to indicate the party a voter belongs to, 
    and real entities like `dbr:United_States_Senate`. 
See 'further elaborations' on how external data is used. 

    
## Inferencing

### Initial Trivial Inferences

*In this section,  a pseudo-formal ad-hoc notation is used to communicate
    steps we want to either infer or deduce.*

These inferences are trivial but enrich the dataset,
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

### Less Trivial Inferences

The following inferences involve arithmetics and gives interesting data from which statistics can be computed from.

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


### Performing an inference-dependent query

These are screenshots of the results of the same query to the same stardog database, 
with (first) and without (second) inferencing. 

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/inference_with.png)

*image 4: Inference proof with inference enabled*

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/inference_without.png)

*image 5: Inference proof with inference disabled*

## Data Reuse

## Data Reuse

To connect our graph to the semantic web, we use existing vocabularies and entity URIs. 

We're interested in 
 - any data about individual voters 
 - text, date, and votes on a bill
 - which voting assembly has which voters and bills
 - which voting assemblies pass legislation for which bills
 
So there's lots of data available. If we were to continue this project beyond the scope of this course, 
we'd want to mine every available source. For now we retrieve data from govtrack, parltrack and dbpedia. 

The process of acquiring this data consists of

 1. identifying candidate sources
 2. evaluating and accessing candidate
 3. coding custom queriers and data constructors for different data sources

Large quantities of data are mined from our current sources, 
and the possibility to combine with more sources remains open.
The number of sources is subject to practically indefinete expansion - until every voting assembly in existence has been covered. 

### Identifying Candidate Sources

One of the first steps in our Agile development approach, was to do some research into the 
the open data provided by governments and political bodies. 
This research helped us with many of our design choices. 
After identifying many possibilities, we narrowed our choices (based on the quality and depth of data) to the following:

- [US Governmental data (GovTrack)](https://www.govtrack.us/)
- [UK Parliament bill progress tracking](http://www.data.parliament.uk/dataset/bills)
- [European Parliament votes on legislative acts](http://parltrack.euwiki.org/)
- [European Council votes on legislative acts](http://data.consilium.europa.eu/)

### Evaluating and Accessing Candidate Sources

|Provider name|endpoint|timblr-stars|comment|
|---|---|---|---|
|GovTrack|http://www.govtrack.us/api/v2/|3|Data encoded in custom JSON format|
|UK Parliament|http://lda.data.parliament.uk/bills.json|3|Data encoded in custom JSON/XML/CSV formats|
|European Parliament|http://parltrack.euwiki.org/dumps/|3|Data encoded in custom JSON/XML/CSV formats|
|European Council|http://data.consilium.europa.eu/sparql|4|Data available through SPARQL endpoint, but is not linked to any external data|
*table 3: sources and their accessibility*

### Motivation for using these sources 

We choose Govtrack and Parltrack as subject of data mining, as 
both contain structued non-semantic voting data relevant to our domain. 
We also construct some data from dbpedia's data. 
The choice of these sources was motivated by their variety in format and uniformity in domain,
and the judgement that we'd be technically able to acquire and mine the data. 

### Data integration methodology

See the Application Functionality section.

#### External Vocabularies and Ontologies

##### Reused Semantic Data

DBpedia is used for the URIs of political parties, state actors and voters, such as
`dbr:United_States_Congress` and `dbr:Democratic_Party_(United_States)>`.
DBpedia is also used for date of birth (`dbp:birthDate`) and gender (`dbo:gender`)
We also use `foaf:gender`.
 

## Querying and Data Analysis 

We now have lots of data which we can analyze by sending complex sparql queries to our database. 
There's no limit to the number of different analyses we can do / queries we can write. 
Below we give some low-hanging ones. 

### Voting Assembly Party Compositions

The following query returns the proportion of parties' representation in a voting assembly at the time of a certain bill. Since the sources are combined into a unified ontology, this will of course work for either of them data sources. Inference is involved: Whether a resource is a voter is never explicitly stored, but is instead inferred from the fact that they vote, because `:votesOn rdfs:Domain :Voter`. 
  
  select ?voting_assembly ?date ?party where {complex condition}

#### Another complex query relying on inferencing

This is a description of the query. 

  select ?stuff where {complex condition}
  
  
## Application Functionality

### Overview

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/designdiagram.png)

*image 6: Overview of program structure*

This diagram illustrates the main structure of our code. 

`__main__.py` is run by a system administrator, who is prompted whether to 
- (re)start the stardog dbms
- reset the database,
- download new data from the data sources, 
- mine(produce/construct/convert) new data from the source data
- initiate LDR , or
- initiate the temporary interface

`interface.py` is a python script using flask to manage `interface.html`. 
`interface.html` is visited by end users, and contains visualizations 
and some pages for certain dataviews. It also links to `LD-R`, through which users
can browse all our data through LD-R's generic data view. 

`database.ttl` is queryable from anywhere by sending a get requests to the endpoint managed by stardog. 

### Data Mining

Data mining here describes the process of generating semantic triples from non-semantic sources. 
Miners retrieve the triples specified in [section](#link). 
The most crucial triples are `Voter voteDirection Votable` and `Votable processedBy VotingAssembly`. 
This is sufficient to form the backbone of the application's graph, to which other data is attached. 
Other data that is fundamental for the domain (i.e. necessities for making the data meaningful) include dates, party memberships, and voter personalia. 
We also link the Polity that that a VotingAssembly legislates for. The latter is among the rarest triples, and is done manually. 
 
#### Space Complexity

This section provides an overview of the size of space complexity of our database in terms of number of triples of each form. 

The number of triples is of order `O(numDatasets*avg_numVotingAssemblies*avg_numBills*avg_numSimultaneousVoters)`

In the case of govtrack, the constants are

    numVotingAssemblies = 2
    numBills = 345k # 170k per voting assembly
    numVotes = 23m #
    numVoters = 12374
    numSimultaneousVoters = 68 # 23m/345k

The mining programs also collecting approximately 5 triples per voter

    voterdata = numVoters * 5 ~~100k
    
This doesn't significantly affect the scale of data, as there are already around 23 million triples. 

##### Scalability Issues?

Is it feasible to have this many triples? [Yes,](http://highscalability.com/blog/2014/1/20/8-ways-stardog-made-its-database-insanely-scalable.html)
up to 50 billion triples is feasible for our database software (stardog). 
     
#### Miners 

The target datasets each needs custom miners, because they are differently formatted. 
From the developers' point of view, the process of mining involves getting the data, inspecting the target datastructure, 

For implementation details, see the miner source codes [in our repository](http://github.com/SW-g16/sw/mine). 

##### Govtrack
    
The Govtrack miner iterates through a very large amount of json files nested in a folder tree. 
The data is organized in Sections of Congress, and Congress is an entity which consists of the two 
voting assemblies; House and Senate. We manually define that they both legislate for the USA. 

The data tree (in which govtrack.us exports their data) has this structure:  

    'congress'
        <int> // range: 1:114 . represents sessions of congress
            'votes'
                <int>|<char> 
                    ('h'|'s')<int>
                        'data.json'
                        
Data about voters is available in a separate `.csv` file. 
Mining this is necessary, as the id used in the voting data (above tree) is only referenced in this file. 
It is also where to find personalia. Therefore it is a prerequisite for enriching our dataset with voter data. 

##### Parltrack

Parltrack provides compressed JSON files, which are kept up to date with the latest data. The parltrack data scrapers gather a vast amount of informtation, with schemas showing the structure found [here](http://parltrack.euwiki.org/dumps/schema.html).

Instead of attempting to learn and integrate something within the existing [Parltrack scraper codebase](https://github.com/civicdataeu/parltrack/tree/master/parltrack), we opted to simply use their data dumps and process the specific parts of those that we were interested in, into linked data.

By consulting the schemas provided and working through their (quite inconsistent) JSON files, we were able to map a large amount of what was needed in the scope of our application. The miner itself processes three Parltrack JSON dumps: votes.json, dossiers.json and meps.json. The only information that can link data between the three data dumps is IDs and since internal IDs are not particularly useful to us, we create some dictionaries, mapping for example, MEP ID to generated MEP URIs. Some of the automatically generated DBpedia URIs were not actually resources, unfortunately. We therefore saved these dictionaries to json files, which can be edited manually with correct URIs.

Thanks to RDFLib, the output is a fully consistent turtle file.

###### Mining Efficiency

The task of mining is desiged to be executed only once for each session of congress. 
This means some inefficiency is tolerable, but it's still an interesting challenge to write an efficient data miner. 
We experimented with multithreading and different channels from python to stardog, but in the end found that
performance was bottlenecked by available hardware. On one common laptop the miner was tested on, initial stable multithreaded mining was achieved, as shown in the screenshot. 

![](https://raw.githubusercontent.com/SW-g16/sw/master/documentation/images/govtrack_multithread.png)

*image 7: multithreaded mining performance on common laptop*

However it would soon slow down significantly, and only one processor core would be active at a time. 
Stardog is not the bottleck, as it claims 300k triples per second. 
If stardog was the bottleneck the, mining process would take 23m triples / 300k triples per second = 83 seconds, 
but for the test laptop it took approximately 50 minutes. 
This leads to the suspicion that the bottleneck is the hardware on which the test was performed, 
but until this is tested it on a more powerful system this cannot be confirmed.
  
###### Implementation issues
    
We found that certain queries yielded results when run on the mined parltrack data, 
but not on the govtrack data, and that this would occur when adding `(2/3 as ?val)` to the outermost select line.
Further, when this query was called stardog would throw a "Divide by 0" error. 
We could not make sense of this behavior, but assume it's due to some unintended feature of the govtrack semantic output. 

###### Enabling inference functionality

During testing, several intended inference functions proved non-functional due to the way the default SL reasoning.type of Stardog handles Equivalence. Only by switching to DL could class membership for, for example, "FemaleVoter" be inferred.


### User Interface

We partially integrated LD-R and we wrote an interface with python with flask, html and js. 
See the screenshots of this report, the appended screencast, and the code on github. 

### Developer environment working scripts

We wrote scripts to automize task sequences that reoccured during development. 
See them in action in the screencast, and the code on github. 
  
## Bonus Assignments

The following section details the degree to which bonus assignments have been fulfilled.

### Linked Data Star

The project produces an endpoint containing previously non-existent triples from both Govtrack and Parltrack, which map to DBpedia and complement/complete existing resources. The added information is mostly in the form of Properties of politicians and their parties.
Overall, the data is in principle publishable, but work on security and further refinement of the ontology would come first. 

### Linked Data Producer

Existing external vocabularies are used with a custom vocabulary in order to construct new semantic data from non-semantic data. 

### Owl Wizard

While there is some inference, it does not fit the 'wizard' requirement.

### Interaction Guru
Users have the ability view data filtered through both our custom data views and LD'Rs default generic views.
Our program inherits the design functionality of LD-R, as well as bootstrapping non-ldr component for aestethic appeal. 
The program includes some basic visualization in the form line plots.
While the program currently does not function at the Guru-level, the interface needed has opened up.
  
## Conclusion

### Goals met

|goal is met|goal|
|-----------|----|
|yes|provide an endpoint that combines voting data from several sources|
|yes|achieve 5 TimBL-stars|
|yes|semantify non-semantic data|
|partially|The data in the endpoint needs to have several meaningful Data Views for humans defined|
|partially|Output to LD-R UI components|
|yes|Analyzing the data |
|partially|Present analysis results in a clear and meaningful way|
|no|Integrate a visual network graph data browser as a LD-R UI component, or apply one if such a component already exists.|

*table 4: project goals and their fulfilment*

We achieved most of our goals with partial success. 
For all goals there is room for practically indefinate refinement - 
 we can combine more sources, we can enrich our data further, we can do more analysis, and we can improve our interface. 
We have successfully established the necessary framework to enable these further refinements. 
 
### Future Development

This project was aborted by a deadline before all goals were met. 
The application is not yet useful. 
Below are the next steps of development we'd take, organized in different categories. 

#### Bug fixes

Different components of our system has worked at different points in time. 
Before expanding functionality, stability and functionality of all components should be verified. 

#### Unit Testing 

Unit tests should be updated and maintained. 

#### Inference

#### Scalability and Hardware

For our final system to run comfortably, it would need more powerful hardware and we'd need change some things. 

#### Interface

##### LD-R

Understand how to configure, and configure. 
This would give developers easier access to data view configurations, 
and would give users a more uniform interface.


##### Integrate WebVowl

Integrating WebVowl to LD-R would give users easier navigation. Tabular and node view could be exchanged interchangably. 

##### Further Analysis

We've opened access to lots of data, and we've only just started to analyze it. 
How do voters and party cluster?

###### Natural Language Processing

Bill texts contain desirable but non-semantic information. 
Tools exist for constructing IRIs to popular graphs like dbpedia from natural lang sentences.  

# Appendix

## Source

 - [GitHub Repository](http://www.github.com/SW-g16/)
    - [ontology](http://www.github.com/SW-g16/ontology.ttl)
    - [sample instance data](http://www.github.com/SW-g16/data/samples)
