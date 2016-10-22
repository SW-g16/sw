import os

import get_session_ids
import constants as c


def wipe_working_tags(session_ids):
    # clears all 'working' tags within the source data set
    # the tags are used to navigate worker threads
    for s_id in session_ids:
        path = '%s/%d/working' % (c.CONGRESS_PATH, s_id)
        if os.path.isfile(path): os.remove(path)


def wipe_done_tags(session_ids):
    # clears all 'working' tags within the source data set
    # the tags are used to navigate worker threads
    for s_id in session_ids:
        path = '%s/%d/done' % (c.CONGRESS_PATH, s_id)
        if os.path.isfile(path): os.remove(path)


def clean():
    session_ids = get_session_ids.get_session_ids()
    wipe_working_tags(session_ids)
    wipe_done_tags(session_ids)
    from subprocess import call
    call(["sh", "sw/scripts/reset-db.sh"])


clean()
