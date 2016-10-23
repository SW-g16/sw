import os

import get_session_ids
import constants as c


def wipe_working_tags(session_ids):
    print "Clearing 'working' tags"
    # clears all 'working' tags within the source data set
    # the tags are used to navigate worker threads
    for s_id in session_ids:
        path = '%s/%d/working' % (c.CONGRESS_PATH, s_id)
        if os.path.isfile(path): os.remove(path)


def wipe_done_tags(session_ids):
    print "Clearing 'done' tags"
    # clears all 'working' tags within the source data set
    # the tags are used to navigate worker threads
    for s_id in session_ids:
        path = '%s/%d/done' % (c.CONGRESS_PATH, s_id)
        if os.path.isfile(path): os.remove(path)

def reset_db():
    from subprocess import call
    print 'Reseting votes db'
    call(["sh", "sw/scripts/reset-db.sh"])


def clean():
    session_ids = get_session_ids.get_session_ids()
    wipe_working_tags(session_ids)
    wipe_done_tags(session_ids)
