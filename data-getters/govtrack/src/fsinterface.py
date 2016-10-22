import os
from os import walk

from flask import json


def get_dirnames(path):
    if not os.path.isdir(path):
        print "Dirnames of non-existing folder requested"
        return None
    try:
        for (dirpath, dirnames, filenames) in walk(path): return dirnames
    except:
        print 'Path existed but caused error: ', path
        return None


def is_int_only_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return None


def get_int_dirnames(path):
    # returns names of all directories within path
    if not os.path.isdir(path):
        print "(get_dirnames) Dirnames of non-existing folder requested"
        return None
    try:
        return sorted([int(d) for d in get_dirnames(path) if is_int_only_str(d)])
    except:
        print  '(get_int_dirnames) Path existed but caused error: ', path
        return None


def loadJsonFile(path):
    if not os.path.isfile(path):
        # print "(loadJsonfile) File doesn't exist",path
        return None
    try:
        f = open(path)
        r = json.load(f)
        f.close()
        return r
    except:
        # print  '(loadJsonFile) Path existed but caused error: ',path
        return None
