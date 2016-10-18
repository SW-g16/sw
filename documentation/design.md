<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Application Design](#application-design)
  - [Goals](#goals)
    - [Primary Goals](#primary-goals)
    - [Secondary Goals](#secondary-goals)
  - [Users](#users)
    - [Target Groups (TG)](#target-groups-tg)
      - [TG_1: People with domain interest](#tg_1-people-with-domain-interest)
      - [TG_2: People with technical interest](#tg_2-people-with-technical-interest)
      - [TG_3: People who are attracted to data visualizations](#tg_3-people-who-are-attracted-to-data-visualizations)
  - [Design](#design)
    - [Browsable Data](#browsable-data)
      - [Explicit Data](#explicit-data)
      - [Inferred data](#inferred-data)
    - [Tabular Browsing](#tabular-browsing)
    - [Network Browsing](#network-browsing)
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

### Target Groups (TG)

We identify these target groups

#### TG_1: People with domain interest

This group wants: 

 - **Facts**: Who voted for what? What passed and what failed, and with what margin?
 - **Analysis**: What patterns exist in the behavior of voters, parties and voting assembles? How do entities cluster and how do values correlate?

#### TG_2: People with technical interest

This group is interested in how the application achieves its functionality. 
We satisfy this need by providing thorough documentation, 
and perhaps by outputing steps of our reasoner's inference. 

#### TG_3: People who are attracted to data visualizations

This group may skip past text and explanations to look at visualizations, regardless of the domain.
This group wants to understand as much information as efficiently as possible from data visualizations.
To satisfy them, we design all our visualizations to be expressive and efficient in communicating data. 
Ideally, the visualizations should also be pretty. 

## Design

Fundamental components of the application include the means to browse 
explicit and inferred data tabularly, (network-)graphically, and statistically.

### Browsable Data

The following data is available for users to browse by different means.

#### Explicit Data

 - Who voted for what
 - Who belongs to what party
 - Who has which external URI (DBPedia, Wikipedia, government pages)
 - ... And probably more as we go along

#### Inferred data

 - What proportion of each party voted for what vote?
 - Proportion of yes/no votes per voter across all bills (to uncover curious cases such as http://www.independent.co.uk/news/world/europe/the-yes-man-romanian-mep-who-has-not-voted-against-anything-in-previous-541-motions-is-accused-of-8899083.html)
 - ... And probably more as we go along

### Tabular Browsing

 - A simple tabular browser, a (set of) interactive table(s)  

### Network Browsing

 - Focus on a node to expand data tool-tip and edges, click again to collapse.
 - Attach meaning to graphical features like color and radius (don't waste dimensions!)

### Devices

Some visualizations will be large and sidebars may have many options, and so we want as large window as possible to display information through. We abide by the mobile-first anyway, as it doesn't cost us much. However the application will be best enjoyed on a large screen, and if there should be design conflicts, consideration of desktop users will be put higher than that of mobile users.

### Possible Extensions

We may consider adding our own API functionality through a SPARQL endpoint, allowing technical users to work with our data in their own applications. Finally, the project will all be open source, allowing anyone to understand and expand on our code-base.

## Walkthrough

On loading the page, the user is presented with an empty main area, and a sidebar to the right. This sidebar contains two drop-down menus, an "add filter" button and a "generate" button. Initially, only the first drop-down menu is accessible. The first drop-down menu allows the user to select a nation. When a nation is selected, the second drop-down menu becomes accessible, allowing the user to select one of the available chambers of government from that nation. As soon as both of these are selected, the "generate" button becomes enabled. Pressing this button will put the program into motion, generating a visual oversight dependent on the selected filters, toggling whether to show, and what to show, about the chamber of government, the politicians within it, and their votes on bills. The "add filter" button allows the user to add more filters so  to provide a clearer oversight of the data, allowing him to select one of a number of filters, such as only showing politicians of specific parties, only showing bills from a specific period, only showing people that voted a specific way on a specific bill, only showing politicians that fit a particular profile (such as wealth, level of education, nation of birth or gender), etc. These filters are then applied the next time the "generate" button is pressed. To the upper left of the screen are save and export buttons, the former allowing the user to save his current selection and filters, the rather exporting an image file of the currently generated political overview.
