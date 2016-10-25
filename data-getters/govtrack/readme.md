the source data has this structure, represented as a file tree. 
all leaves are named data.json. 

'congress'
	<int> // range: 1:114 . represents sessions of congress
		'votes'
			<int>|<char> 
				('h'|'s')<int>
					'data.json'
					
the govtrack getter traverses 'congress' to find all data.json files nested as in the above tree.
together, these data.json files contain all votes, all bill texts, and mentions of all voters. 

for more information about the voters, we mine congress-legislators.csv. 
this file contains more information, including personalia like gender and age, as well as party membership and wikipedia links

