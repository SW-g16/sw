import os



import threading
lock = threading.Lock()

class Miner(object):
    """The superclass of all miners


    """

    DIR_PATH = os.path.dirname(os.path.abspath(__file__))
    TEMP_FILENAME = 'temp'
    MEMORY_CAP = 0.5
    TRIPLES_PER_UPLOAD = 20000

    def __init__(self, db, namespaces, test=False):
        self.namespaces = namespaces
        self.db = db
        self.triples = set()
        self.test = test

    def add_triple(self,triple):

        lock.acquire()
        try:
            self.triples.add(triple)
            if len(self.triples) >= self.TRIPLES_PER_UPLOAD:
                self.add_to_db(self.triples)
                self.triples = set()
        except Exception as e:
            print 'Unenxpected error'
            print e.message
            lock.release()
            raise Exception()
        lock.release()


    def add_to_db(self, trips):

        lock.acquire_lock()
        try:
            if len(trips) == 0:
                return
            print 'Forwarding %s trips from %s to stardog' % (len(trips), type(self).__name__)
            fn = '%s/%s_%s.ttl' % (self.DIR_PATH, self.TEMP_FILENAME, type(self).__name__)
            with open(fn, 'w') as f:
                f.write('%s\n%s' % (self.namespaces.PREFIX_LINES, ('\n'.join(trips)).encode('utf-8')))
            self.db.data_add(fn)
            os.remove(fn)
        except Exception as e:
            print 'unexpected error %s' % e.message
        lock.release()