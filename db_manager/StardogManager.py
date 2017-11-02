from SPARQLWrapper import SPARQLWrapper, JSON

from SemanticDatabaseManager import SemanticDatabaseManager, DatabaseDoesntExistException, DatabaseServerIsntRunningException

import os
import threading
lock = threading.Lock()

class StardogManager(SemanticDatabaseManager):


    # todo lock resources more neatly and be sure that each lock is needed


    CMD_QUERY = 'stardog query %s "%s"'
    CMD_SERVER_START = "stardog-admin server start --disable-security"
    CMD_NAMESPACE_ADD = "stardog namespace add --prefix %s --uri %s %s "
    CMD_SERVER_STOP = "stardog-admin server stop"
    CMD_DB_CREATE = "stardog-admin db create -n %s"
    CMD_DB_DROP = "stardog-admin db drop %s"

    MISSING_ENVIRON_MESSAGE = '''
    
    # One or more environment variables need to be set. 
    # You can do this by adapting the following lines for your system and executing them
    # Assuming you're running some linux distribution
    
    export PATH=$PATH:~/Software/stardog-5.0.4/bin/ # or wherever you've got Stardog 
    export PATH=$PATH:/usr/lib/jvm/java-8-openjdk-amd64/bin/ # or whatever java installation. Stardog needs java 8
    export STARDOG_HOME=~/Software/stardog-home/ # any new directory
    '''.replace('\n'+' '*4,'\n')

    STARDOG_URL = 'http://localhost:5820'


    def data_add(self, path):
        if not self.is_quiet: print 'Adding data'

        lock.acquire()

        res = self.cmd('stardog data add %s %s' % (self.db_name, path))

        lock.release()

        if res == 0:
            if not self.is_quiet: print 'Added data'
        else:
            raise Exception('Failed to add data')


    def __init__(self, db_name, namespaces):
        super(StardogManager, self).__init__()
        self.db_name = db_name
        self.namespaces = namespaces
        self.__q_conn__ = SPARQLWrapper('%s/%s/query' % (self.STARDOG_URL,db_name))

    def tear_down(self):


        if not self.is_quiet:
            print 'Tearing down db.'
        print 'If execution hangs here for more than 30 seconds then stardog might be unresponsive. Close the terminal session and try again. '

        # todo be more certain that exceptions are correct
        lockpath = "%s/system.lock" % os.environ['STARDOG_HOME']
        if os.path.isfile(lockpath):
            os.remove(lockpath)
        failed_to_drop = self.cmd(self.CMD_DB_DROP % self.db_name)

        failed_to_stop = self.cmd(self.CMD_SERVER_STOP)

        if failed_to_stop:
            # assume the server wasn't running
            raise DatabaseServerIsntRunningException()
        elif failed_to_drop:
            # failed to drop the database, but not because server wasn't running.
            # assume the database didn't exist in the first place
            raise DatabaseDoesntExistException()

        if not self.is_quiet: print 'Tore down db'

    def set_up(self):

        def assert_requirements_met():
            assert self.cmd('java') == 1, 'Java not installed, or not set in PATH. \n%s' % self.MISSING_ENVIRON_MESSAGE
            assert 'STARDOG_HOME' in os.environ.keys(), 'STARDOG_HOME environment variable not set. \n%s' % self.MISSING_ENVIRON_MESSAGE
            assert self.cmd('stardog') == 0, 'Stardog not installed, or not set in PATH. \n%s' % self.MISSING_ENVIRON_MESSAGE
        if not self.is_quiet: print 'Setting up db'
        assert_requirements_met()
        
        try:
            assert self.cmd(self.CMD_SERVER_START) == 0, 'Failed to start stardog server'
            assert self.cmd(self.CMD_DB_CREATE % self.db_name) == 0, 'Failed to create database'
            if not self.is_quiet: print 'Set up db'
        except:
            if not self.is_quiet: print 'Failed to set up stardog, shuting it down and retrying'
            self.tear_down()
            self.set_up()
            if not self.is_quiet: print 'Finally succeed in setting up DB'
            return
        for key in self.namespaces:
            if not self.is_quiet: print 'Adding namespace %s' % key
            assert self.cmd(self.CMD_NAMESPACE_ADD % (key, self.namespaces[key], self.db_name)) == 0, 'Failed to add namespace'
            if not self.is_quiet: print 'Added namespace %s' % key

    def select_query(self, query):
        if not self.is_quiet: print 'Passing select query to stardog %s'

        lock.acquire()
        self.__q_conn__.setQuery(query)
        self.__q_conn__.setReturnFormat(JSON)

        error = None
        r = None
        try: r = [{key:result[key]['value'] for key in result} for result in self.__q_conn__.query().convert()["results"]["bindings"]]
        except Exception as e: error = e

        lock.release()
        if error is not None:
            if not self.is_quiet: print 'Select query failed! %s' % error.message
            raise error
        assert r is not None
        return r

    def insert_query(self, query):

        lock.acquire()
        error = None
        try:
            assert self.cmd(self.CMD_QUERY % (self.db_name, query)) == 0
        except Exception as e:
            error = e

        lock.release()

        if error is not None:
            if not self.is_quiet:
                print 'Insert query failed! %s' % e.message
            raise error