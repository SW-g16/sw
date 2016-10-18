<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Browsable Data](#browsable-data)
  - [Explicit Data](#explicit-data)
  - [Inferred data](#inferred-data)
- [Tabular Browsing](#tabular-browsing)
- [Network Browsing](#network-browsing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

// bits and pieces

////////////////////////////////////////

Different data providers provide data in different formats.
This means both that we have to hand-write aligners/mappers/getters for each different data source, 
and that our application will result in production of useful semantic data. 


///////////////////////////////


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
