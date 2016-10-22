import time

from src import govtrack_processor

start = time.time()
print 'starting import...'
govtrack_processor.init()
print 'all workers are done. the entire govtrack dataset should now have been mined'
print 'took ', time.time() - start, 'seconds'
