import sys
import time

import get_session_ids
import p_congress

print 'Govtrack Data Miner'

print 'Mining Voters...'

import p_voters
import os

if raw_input('will (over)write to data/govtrack/govtrack.ttl. Proceed? (y/n)\n') is 'y':

    output_path = os.path.dirname(os.path.abspath(__file__))+'/../../data/govtrack/govtrack.ttl'
    print output_path
    with open(output_path, 'w') as f:
        # Note that f has now been truncated to 0 bytes, so you'll only
        # be able to read data that you wrote earlier...
        f.write('')
        f.close()
else:
    print 'Aborting. '
    exit(0)

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
