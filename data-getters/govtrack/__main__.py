import sys
import time

from src import get_session_ids
from src import p_congress

print 'Govtrack Data Miner'

print 'Mining Voters...'

from src import p_voters

p_voters.process_voters()

start = time.time()

# get the list of session ids
session_ids = get_session_ids.get_session_ids()

if len(sys.argv) > 1:
    # num_session/5 threads (== 114/5 == 23 threads)
    start_index = int(sys.argv[1])
    p_congress.process_congress(session_ids[start_index * 5:start_index * 5 + 5])

else:
    # single thread
    p_congress.process_congress(session_ids)