import time
import sys
from src import get_session_ids
from src import govtrack_processor

print 'Govtrack Data Importer'

start = time.time()

# get the list of session ids
session_ids = get_session_ids.get_session_ids()

if len(sys.argv) > 1:
    # num_session/5 threads (== 114/5 == 23 threads)
    start_index = int(sys.argv[1])
    govtrack_processor.init(session_ids[start_index * 5:start_index * 5 + 5])

else:
    # single thread
    govtrack_processor.init(session_ids)

print 'Done after', time.time() - start, 'seconds'
