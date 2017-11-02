# Voting Data Aggregator

Originally written for the Semantic Web course of 2016 at VU Amsterdam. 
Revised November 2017. 

## Description

This repo includes a semantic ontology (ontology.ttl) which defines central concepts related to parlamentary voting.

The code here does the following

 - downloads historical voting data from parltrack.com and govtrack.com (different data and formats)
 - extracts triples fitting the custom ontology from both
 - combines extracted triples into a semantic database 
 - runs an interface for browsing the database and viewing some basic statistics on the data

An LD-R instance was also partially configured. TODO review 

## Revision note November 2017

Major rewrite of miners. Interfaces left untouched, and are atm not functional. 
TODO do todos below to fix. work in progress

## Installation

You will need Stardog (community edition), Java and Python on your system. 

    # cd to wherever you want to install
    git clone https://github.com/SW-g16/sw.git
    cd sw
    pip install -r requirements.txt


## Testing 

Test runs of the miners mine a subset of the available data. 
The amount of data to mine can be configured by changing the `test` variable within the test scripts. 
The `test` variable indicates the number of objects ParlTrackMiner iterates through before stoping. 
When `bool(test)==True`, GovTrackMiner mines data from a certain date (2017-08-01) and until today. 
This can be configured in the init function of GovTrackMiner. (TODO set in test scripts instead, or set date based 
on the `test` variable, for example set date to `test` days ago)

    # test each function of each miner sequentially
    # (5 sequentally run tests 
    #   (parltracks 3 subtasks and govtracks 2 subtasks run separately))
    python -m unittest test_miners_granularly
    # all tests pass after ~ 125 seconds when test=1000
    
    # test multithreading of each miner
    # (2 sequentially run tests, where each test involves multithreading 
    #   (parltracks 3 subtasks run in parallel, then govtracks 2 subtasks run in parallel))
    python -m unittest test_each_multithreaded_miner
    # starts mining but soon hangs indefinetly, presumably due to some mistake in applying locks
    
    # test multithreading of multithreaded miners
    # (1 test, performing parltracks 3 subtasks and govtracks 2 subtasks in parallel)
    # starts mining but soon hangs indefinetly, presumably due to some mistake in applying locks
    
By default, the database is left intact and the stardog remains running after the tests are done. 
This enables you to inspect the database and use the interface after the tests have added data. 
To destroy the database after a test, set the `DESTROY_DB_AFTER_TESTS` variable to `True`. 

To inspect the database with stardog's interface, visit `localhost:5000` in your browser. 
To use the interface, run this command: 

For more verbose terminal output, toggle the parameter to `self.set_quiet()` in `SemanticDatabaseManager.py` to `False`

## Full run

    # this will take several hours
    python .
    # not testing after rewrite, might fail

## TO-DOs

 - fix multithreading bugs
 - Ensure the URIs used by the miners are consistent with the ontology
 - Catch and process terminal output from `subprocess.call()` calls by the miners, to make terminal neater
 - integrate `parltrack_download.sh` with the functions in `ParlTrackMiner` that uses them, get rid of the .sh file
 - implement what's described in `party-issue.md`
 - extend documentation (better readme's, in-code commenting and docstrings)
 - clean up the old `documentation` folder
 - configure the LD-R instance to make it useful
 - review/revise the ontology
 - more data sources/mining scripts
 - more interesting statistics
 - review/revise the interface 
 - consider switching to a FOSS triplestore
 