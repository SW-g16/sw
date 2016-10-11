# Application Design
*Semantic Web Course 2016*

*Group 16 - Eirik K. Kultorp (2544992), Ross G. Chadwick (2533539), Ramses IJff (2545868)*

## Introduction

Many governments have began to provide endpoints for their internal data as a way to become more transparent and push for greater public participation, and voting data is amongst the large amount of data available for big data processing. We would like to use this opportunity to mine the (and others) public open database of votes, as provided by some states. We'll be providing the data both as a computer-friendly API and human-friendly visualizations. We will both forward data of the external data sources, and provide new generated semantic data by inference.

## Goals

The goal of our application is to provide users with a means to efficiently get both an overview and detailed knowledge of voting data provided by states. We want to give users both an intuitive insight into the (mostly machine-readable) governmental data through in-depth visualization, and to provide them with the possibility to browse data tabularly in a way that's more user-friendly than that provided by the original data provider. Furthermore, we aim to apply machine-reasoning (inference) to arrive at information that is fundamentally important and interesting when researching voting systems, but not made explicit in the original dataset. We would also aim to combine and compare data on different voting entities, for example, The British Parliament, American Senate and more (which provide open data). It is (very) difficult to automatically map strings as having equivalent meaning, but we could collect "equivalent-to" or "equivalent-intention-to" between laws of different databases/states. As a meta-goal, we also want to employ our application on the web to share it with others.  

## Users

### Target Groups (TG)

Below, we have identified some target groups:

#### TG_1: People with domain interest

This group wants to know

 - Who voted for what?
 - How homogeneous were the party members in their votes?
 - Which clusters of similar voters exist?

This is information that we will infer. We will elaborate on inference further into this document

#### TG_2: People with technical interest

This group is interested in how the application achieves its functionality. We satisfy this need by an extensive about-page, documenting it's workings. We may also show steps taken by the reasoner to arrive at different inferred knowledge.

#### TG_3: People who are attracted to aesthetically pleasing visualizations

This group may skip past text and explanations to look at visualizations, regardless of the domain.
This group wants to understand as much information as efficiently as possible from data visualizations.
To satisfy them, we design our visualizations to be self-explanatory and use graphical features of graph elements (x,y,radius,color,link distance, etc) as keys for different dimensions of data.

## Design

Fundamental components of the application include the means to browse explicit and inferred data tabularly, (network-)graphically, and statistically.

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
