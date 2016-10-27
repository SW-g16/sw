import sys
import time

import get_session_ids
import p_congress

print 'Govtrack Data Miner'

print 'Mining Voters...'

import p_voters

p_voters.process_voters()

start = time.time()

# get the list of session ids
session_ids = get_session_ids.get_session_ids()[:1] # mine only 5 congress sessions to save resources while developing
print session_ids

if False: # true for multithread
    # num_session/5 threads (== 114/5 == 23 threads)
    start_index = int(sys.argv[1])
    p_congress.process_congress(session_ids[start_index * 5:start_index * 5 + 5])

else:
    # single thread
    p_congress.process_congress(session_ids)
