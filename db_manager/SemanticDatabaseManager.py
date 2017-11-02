import os
import sys
import subprocess

class DatabaseDoesntExistException(Exception): pass


class DatabaseServerIsntRunningException(Exception): pass



import threading
lock = threading.Lock()

class SemanticDatabaseManager(object):

    # the superclass of all database managers

    # to facilitate for possible future replacement of stardog with something else

    QUIET = open(os.devnull, 'wb')
    ERR_OUT = sys.stderr
    STD_OUT = sys.stderr

    def __init__(self):
        self.set_quiet(True)

    def set_quiet(self, be_quiet):
        if be_quiet:
            self.is_quiet = True
            self.std_out = self.QUIET
            self.err_out = self.QUIET
        else:
            self.is_quiet = False
            self.std_out = sys.stdout
            self.err_out = sys.stderr

    def cmd(self, cmd, quiet=None):

        lock.acquire_lock()

        if quiet:
            r = subprocess.call(cmd, shell=True, stdout=self.QUIET, stderr=self.QUIET)
        else:
            r = subprocess.call(cmd, shell=True, stdout=self.std_out, stderr=self.err_out)

        lock.release()

        return r