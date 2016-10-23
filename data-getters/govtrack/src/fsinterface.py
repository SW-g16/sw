import os
from os import walk

from flask import json


def get_dirnames(path):
    for (dirpath, dirnames, filenames) in walk(path): return dirnames

def is_int_only_str(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_int_dirnames(path):
    dirnames = get_dirnames(path)
    if dirnames is None: return []
    return sorted([int(d) for d in dirnames if is_int_only_str(d)])


def loadJsonFile(path):
    f = open(path)
    r = json.load(f)
    f.close()
    return r
