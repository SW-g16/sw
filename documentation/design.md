<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Application Design](#application-design)
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

<!-- END doctoc generated TOC please keep comment here to allow auto update -->


# Application Design
*Semantic Web Course 2016*

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

## Goals

### Primary Goals

 - Provide an endpoint combining open voting data from different sources
 - Achieve 5 timbl-stars
 - Define meaningful Data Views for humans
 - Output data views to LD-R UI components
 
### Secondary Goals
 
 - Integrate a visual network graph data browser as a LD-R UI component, or apply one if such a component already exists
 - Analyze the data using machine learning techniques for semantic data
 - Define Data Views for viewing statistics / interesting output of analyzing machine
 - Visualize statistics / analyzer output with standard plots and charts within a LD-R UI component. 
 
## Users

### Satistfaction Requirements

We identify some satisfaction requirements that some user may have. 

 - **Facts**: Who voted for what? What passed and what failed, and with what margin? 
 - **Analysis**: What patterns exist in the behavior of voters, parties and voting assembles? How do entities cluster and how do values correlate?
 - **Shareability**: possibility of sharing views with others
 - **visualization**: visualizations make structures in data easier 
 - **Documentation**: We thoroughly document our app's functionality. 
 - **Code accessibility**: We make our code readable and available under an open license on GitHub
 
We define some Target Groups. 
 

#### TG_1: People with domain interest

These users are interested in the data itself, and in any patterns that can be seen in it. 
They view visualizations as tools to understand the data, and are unlikely to care about the machine's inner workings. 

#### TG_2: Developers

These take an interest in how our application works and might want to view or use our code. 
They inherit the needs of all other users. 

#### TG_3: People who are attracted to data visualizations

This group may skip past explanatory text to look at visualizations, regardless of the domain.
This group wants to understand as much information as efficiently as possible from data visualizations.

### Satisfaction Requirements per Target Group

The TGs have these SRs, in no particular order. 

|Target Group|Fact|Analysis|Sharability|Visualization|Documentation|Code Accessibility|
|---|---|---|---|---|---|---|
|TG_1|1|1|1|1|0|0|
|TG_2|1|1|1|1|1|1|
|TG_3|0|1|1|1|0|0|

#### Implied Technical Requirements (TRs)

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

## Design

### The LD-R Framework

We use the LD-R framework to avoid reinventing wheels. 
Web pages are generated for us, after we apply our custom configurations. 

#### Code Location / Method

We design our interface by modifying config files of LD-R. 

#### Network Graph Browser

We may integrate some semantic network graph browser as an LD-R component. 
[WebVOWL](http://vowl.visualdataweb.org/webvowl/index.html) seems relevant. 

#### Text-based Browser

We create Data Views that generate tabular and object 'profile pages'. 

### Devices

Our application inherits the mobile-first layout of LD-R. 
However for some visualizations it is sometimes desirable to have a larger screen,
as it allows for communicating more information at once. 

### Possible Extensions

We may consider adding our own API functionality through a SPARQL endpoint, 
allowing technical users to work with our data in their own applications. 
Finally, the project will all be open source, 
allowing anyone to understand and expand on our code-base.

## Walkthrough

A user lands on the main page and is presented with an overview of the data. 
The user clicks a link to an entity and sees all relevant data (defined by a Data View) associated with it, 
    including inferred statements. 
There is also a set of graphs and statistics available. 
The user finds these interesting, and copies the url currently in the address bar and posts to their friend.
 the friend sees the same data in the same way as the first user, and they both like the link on facebook. 

The user wants to generate a graph of data defined by applying user-defined filters on the dataset. 
The user sets their filters.
The filters include restrictions like only showing bills from a specific period, only showing people that voted a specific way on a specific bill, 
     only showing politicians that fit a particular profile (such as wealth, level of education, nation of birth or gender), 
The user hits submit. 
Upon a warning, the user realizes they were about to init getting and rendering of a very large amount of data and hit cancel. 
They modify their filter and retries. 
A semantic graph is returned, and sent to our WebVowl component for visualization. 
