
# Status

We map our status relative to the rubrics. 

> The requirements set out per milestone correspond to the rubric categories that we will grade the final report by.

We mark where we think we currently are with an x, based on to what extent we followed the individual subrequirements below. 

0/-10 means -10 points for ontology and inferencing, 0 points for the other rubrics.  

The grade estimate is brutal for our own good. 
0 is given if the requirement is only fulfilled implicitly in some other part of the document, or if there is inaccuracy. 

|Rubric										|0/-10 none|5/2 novice|11/6 competent|10/20 proficient|
|----|--------------------------------------|----------|----------|--------------|----------------|
|Report organization, layout and language	|		   |	      |	 		     |				  |
|Description of the application and users	|		   |	      |	 		     |				  |
|Design and walkthrough					 	|		   |	      |	 		     |				  |
|Domain and conceptualization				|		   |	      |	 		     |				  |
|Ontology and inferencing					|		   |	      |	 		     |				  |
|Data reuse									|		   |	      |	 		     |				  |
|Queries 									|		   |	      | 		     |				  |
|Application functionality					|		   |	      | 		     |				  |
|Linked Data Star							|		   |	      |	 		     |				  |
|Linked Data Producer						|		   |	      |		         |				  |
|Owl Wizard									|		   |	      | 		     |				  |
|Interaction Guru  							|		   |	      |	 		     |				  |

## Subtasks / tips

Identified todos are in tables. (Reformulated) tips, guiding questions and other quotes from blackboard are in > quotes. 

### Report organization, layout and language

> Word counts are just an indication. If below limit, prolly u didn't say all. if above, prolly too verbose
> Report should be ca 8-12 pages
> Don't be unecessarily verbose 


// tables, screenshots, and quotes are nice
// be as concice as possible 
// avoid narrative language: avoid 'we' and other references to us as much as possible
// don't be afraid of lot of headers with small or no paragraphs: they help significantly to maintain the structure of our report, making it more modular. this makes it easier to navigate, read and write 
// designing the report like a tree is also a relatively w3-friendly document format

|Category|Grade estimate|Description|Comment|
|--------|-----|-----------|------|
|language|~|use academic/professional english||
|structure|+|report's header tree corresponds to rubrics and their subrequirements|todo complete building report skeleton|
|graphics|+|include relevant plots n charts and other images (but only when it makes sense)|todo make and include all required|
|write|~|have conclusion: which goals we met and what further work would be done|todo expand|

### Description of application and users

> the goal of the application: what does it do? What task does it perform?
> the users of the application: for whom is the application intended? (people, machines, mobile users). 
> How does the application satisfy a need of the users?

|Category|Grade estimate|Description|Comment|
|--------|-----|-----------|------|
|write|~|define goals of application|goals were written weeks ago. needs update.|
|write|-|describe functionality (high abstraction level)|keep brief, details come in Application Functionality section|
|write|~|define target groups|is elaborate but needs refinement and maybe expansion|

### Design and Walkthrough

> the design of the application: what does it look like
> how does it present information to users (what views of the data are presented)
> give a walkthrough of how users will interact with the application 
> justify the design and views. why do they make sense? 

// 0's are given to some writing todos below, because they're based on the premise that we have a successfully configured LD-R interface.
// it needs rewriting to clarify what we have and what we intend to have

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|code |+|encode and use views|is done for a few views in non-ldr fiddle|
|write|-|describe and justify LD-R|see the docs. there is little description or justification, only endorsement|
|write|-|give abstract definitions of views|doesn't exist|
|write|~|give exact defintion of views|is done unelegantly with screenshots. todo give formal definition|
|write|+|give walkthrough|is integrated with the rest of the section|
|write|~|justify design and views|explain that fiddle was last minute patch, that better solution is use ld-r bcs code reuse. see 'describe and justfy ldr' req above|

// Our main product is a module, rather than an application for users. 

### Domain and coceptualization

> describe the domain and scope of the ontology, as determined by the application
> describe the methodology that is used in the construction of the ontology 
> description of the ontology
> diagram(s) of the ontology

// scope and domain seems mostly covered, but are somewhat merged when they shouldn't be. 
// also needs more clear structure

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|write|~|describe scope|todo review|
|write|~|describe domain|todo review|
|chart|-|put diagram of ontology||
|write|~|describe ontology|done to some extent. reference diagram when up. |

### Ontology and inferencing

> have at least 15 classes and at least 5 properties 
> have an ontology that explicitly represents the conceptualization in OWL
> Use at least 5 class restrictions
> The ontology should reuse at least 3 existing vocabularies or ontologies. 
> Describe the ontology, and the decisions made 
> the ontology should produce meaningful inferences that are essential for the application. 
> This should be evidenced by a screenshot of e.g. Protege reasoning results. Describe the inferences (100-500 words) 
> NB: For the final report: inferences should be on the external data

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|Ontology|-|have 15 classes|we have 9 classes|
|Ontology|+|have 5 class restrictions|(todo verify this is covered)|
|Ontology|2/3|reuse 3 vocabularies or ontologies|we have foaf and dbpedia. need one more.|
|Ontology|~|describe the ontology design and the decisions behind it|is elaborate but needs updating|
|Inference|~||needs distinction between what's inference and deduction, and deduction should go elsewhere. needs distinction between what we have done and what we want to do. (we currently only have trivial uninteresting inferencing (but it is crucial))|
|Inference|+|Give screenshots evidencing inference||
|Inference|-|Infer on external data||

### Data Reuse

> describe at least 2 external sources, where at least one is semantic
> give motivation for choice of data sources: why does the application need these sources specifically?
> describe how we integrated the data with our ontology. inference?

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|Research|~|describe 2 sources|we describe parltrack, govtrack and dbpedia. needs better structure and a comparison table|
|write|~|motivation for choosing these source|needs refinement|
|write|~|data construction methodology (bried)|keep brief. elaboration in Application Functionality|

### Queries

> several documented(commented) SPARQL queries relevant to the application, that produce results over the integrated data and ontology
> proof that queries depend on inference (screenshot reasoning on/off)
> discuss inferences made

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|Query writing|+||Some queries exist, but they need more documentation, and should be more in numbers|
|Inference|+|Proof that queries depend on inference (screenshot)|we have this for a trivial query|
|Query writing|-|Make complex query that depends on inference||
|write|-|discuss inferences made|needs discussion|

### Application functionality

> Have a working prototype of the application (nothing to hand in)
> A screencast of the working application (max. 2 minutes)
> A Turtle file that contains the final ontology
> A link to the source files of the application (online) 

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|code|+|have working prototype|fix govtrack (but this is only a module, not the main program)|
|code docs|+|describe|put and reference system diagram|
|screencast|-|show program functionality|needs making|
|ontology|+|have ontology.ttl with and without sample data||
|write|~|describe ontology construction methodology|done generically for miners, specifically for govtrack, but not specifically for parltrack| // moved here from 'domain and inferencing'

### Extra points


> Groups of 4 have another requirement for another 10 points. 
> This means that groups of four need to achieve 100 points to be able to get a grade of 10 (instead of 90 points).
> This needs to be present as an explicit section in the final report 
> You can choose one of the following:

// It looks like we have another 40 points theoretically available for us. 

// note that each needs writing about. 

##### Linked Data Star

> publish the ontology & data that has value for others
> make the data available as dereferencable URIs, enrich the data with e.g. mappings to other data sources, but also meta-data (using VOID), use provenance information, etc.

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|data publishing|-|make endpoint available online|can be done by free serverhosting|
|data publishing|+|make data dereferencable and enriched with mappings to external sources|done locally|

##### Linked Data Producer 

> convert an existing non-RDF dataset to RDF
> use existing vocabularies to model its content.

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|code|+|semantify non-semantic data|done in govtrack and parltrack|
|publishing|~|use existing vocabularies in the semantification|we did, but also used some we defined ourselves|

##### OWL Wizard

> make a very rich and expressive ontology, that allows your application to derive non-trivial results. The more expressive the ontology the better

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|Inference|-|do lots of inference|we make only some trivial inference|
|Data analysis|~|derive non-trivial results|we compute some basic statistics that border on the trivial|

##### Interaction Guru 
 
> the more visually appealing and interactive the application, the better. Think of cool, innovative ways to interact with the data that is used by your application.

// We have the framework, data and queries, but fail to glue it together. Our pretties pages are bootstrap tables|
// we should consider to make a separate fiddle with some visualizations. 

    to develop more interesting visualizations and data views. 

|Category|Grade estimate|Description|Comment|
|--------|--------------|-----------|------|
|Interface|+|enable users to browse data|through ld-r. needs more custom views and searching for efficient user navigation|
|Interface|+|configure data views|by outputing custom tables, we're effectively defining views|
|Design|+|have neat design|we inherit the neat desidn of ld-r, and bootstrap the non-ldr components|
|visualization|~|visualize some data as excellently as possible|we give some basic line plots of some statistics through time|
