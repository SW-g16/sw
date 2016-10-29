import requests
import time

import constants as c

def save(triples):
    start = time.time()
    rdf = ''.join(["%s %s %s.\n" % (t[0], t[1], t[2]) for t in triples if len(t) == 3])

    duration = time.time()-start
    print 'constructing rdf took %f sec' % duration
    start = time.time()
    with open(c.DATA_PATH+'/govtrack.ttl', 'a') as the_file:
        the_file.write(''.join([i if ord(i) < 128 else '' for i in rdf]))

    print 'writing to file took %f sec ' % (time.time()-start)