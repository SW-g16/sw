Representatives are typically associated with political parties.

Often there are several associations over time, both because of switch of party and because of a party changing name.

Therefore it's necessary to be able to store more than one party association per representative, and to store the time period of an association.

The easiest way to do this is by storing structures like this:

    <some_representative> votes:party_association [
        a votes:Party_Association;
        votes:party <some_party>;
        votes:party_association_period [
            a votes:Party_Association_Period;
            votes:start_time "1999-08-16"^^xsd:date;
            votes:end_time "2001-01-02"^^xsd:date.
        ]
    ]

This includes two b-nodes (nodes without a declared uri).
In some datebase systems, URIs are automatically created for b-nodes, so the above structure could easily be inserted.
However this is not the case with Stardog - Stardog does not support b-nodes.

Therefore it's necessary to manually create uris for the b-nodes. This is tedious but can be done, with the same process as in [my other project](https://github.com/Ysgorg/AIF-API/blob/master/aifapi/AnAIFdb/AnAIFdb.py)

The method would be like this: 

    keep track of party associations while mining data, but don't add it to db yet
    
    after mining task is done:
        
        if there were no other party association objects in the database:
            party_association_auto_id = 1
        else:
            party_association_auto_id = 1 + query('select ?auto_id where {?party_association votes:auto_id ?auto_id. ?party_association a votes:Party_Association} order by desc(xsd:integer(?auto_id))')['auto_id']
            
        if there were no other party association time period objects in the database:
            party_association_time_period_auto_id = 1
        else:
            party_association_time_period_auto_id = 1 + query('select ?auto_id where {?party_association_time_period votes:auto_id ?auto_id. ?party_association a votes:Party_Association_Time_Period} order by desc(xsd:integer(?auto_id))')['auto_id']
        
        for each newly mined party association:
        
            representative_uri = # unique uri already obtained
            party_association_uri = party_association_<party_association_auto_id>
            
            insert_data(
                representative_uri votes:party_association party_association_uri.
                party_association_uri a votes:Party_Association.
                party_association_uri votes:auto_id party_association_auto_id.
            )
            
            for each associated party association time period
            
                party_association_time_period_uri = party_association_time_period_<party_association_time_period_auto_id>
                
                insert_data(
                    representative_uri votes:party_association party_association_uri.
                    party_association_uri a votes:Party_Association.
                    party_association_time_period_uri votes:auto_id party_association_time_period_auto_id.
                )
                
                
                party_association_time_period_auto_id += 1
            
            party_association_auto_id += 1

in parltrack, we at least already have available the periods of each association. 
in govtrack, this isn't available and we'd first have to look at the party association field for every vote_voter object of the representative (one for every time they voted on something). 




...


! 

perhaps it's only sparqlwrapper that doesn't like b-nodes. todo check in stardog docs
