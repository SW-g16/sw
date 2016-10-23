import time

import sys

from src import get_session_ids

from src import govtrack_processor, resetdb

print 'Govtrack Data Importer'
#if raw_input("Reset state first? (y/n): ") == 'y': resetdb.clean()
start = time.time()
session_ids = get_session_ids.get_session_ids()

start_index = int(sys.argv[1])
govtrack_processor.init(session_ids[start_index*5:start_index*5 + 5])

print 'all workers are done. the entire govtrack dataset should now have been mined'
print 'took ', time.time() - start, 'seconds'
