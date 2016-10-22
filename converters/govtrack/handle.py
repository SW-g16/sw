

import govtrack
import time

start = time.time()
govtrack.constructData()
print 'all workers are done. the entire govtrack dataset should now have been mined'
print 'took ' , time.time()-start,'seconds'
