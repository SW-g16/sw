import os
import thread

import session_processor
import get_session_ids

global thread_status_dict
global num_active_threads
global num_win_threads
global num_fail_threads

thread_status_dict={}
num_active_threads=0
num_fail_threads=0
num_win_threads=0

import constants as c
import fsinterface

def mark_session(session_id, key):
    if key == 'working':
        # the thread is starting work on this branch
        # we mark it so other threads stay away from this session
        f = open("%s%d/%s" % (c.CONGRESS_PATH, session_id, key), 'w')
        f.close()
        return True
    elif key == 'done':
        # the thread is done with this branch
        # we mark it as done so other threads stay away from this session, also upon a later run of this program
        f = open("%s%d/%s" % (c.CONGRESS_PATH, session_id, key), 'w')
        f.close()
        if os.path.isfile("%s%d/working" % (c.CONGRESS_PATH, session_id)):
            os.remove("%s%d/working" % (c.CONGRESS_PATH, session_id))

        return True

    else:
        # print "invalid key: ",key
        return False


def change_num_active_threads(val):
    global num_active_threads
    num_active_threads = num_active_threads + val


def change_num_win_threads(val):
    global num_win_threads
    num_win_threads = num_win_threads + val


def change_num_fail_threads(val):
    global num_fail_threads
    num_fail_threads = num_fail_threads + val


def worker(s_id):
    global thread_status_dict
    global num_active_threads

    thread_status_dict[s_id] = 1

    def fail(message):
        # print message
        change_num_active_threads(-1)
        change_num_fail_threads(1)
        return False

    def win():
        change_num_active_threads(-1)
        change_num_win_threads(1)
        return True

    try:

        # indicate that a worker is already processing this session

        if mark_session(s_id, 'working') is False: return fail('failed to set work tag %d.' % s_id)

        session_processor.process_session(s_id, c.EMPTY_THRESHOLD)

        # indicate that a worker has completed processing this session

        if not mark_session(s_id, 'done'):
            return fail('failed to set done tag %d. ' % s_id)

        # received response from stardog

        thread_status_dict[s_id] = 2

        # return win signal

        return win()
    except:
        return fail('no')


def terminalUpdate():
    print '%d active threads, %d completed threads, %d failed threads' % (
    num_active_threads, num_win_threads, num_fail_threads)


def init():
    global num_active_threads
    global num_win_threads
    global num_fail_threads
    global thread_status_dict

    num_fail_threads = 0
    num_win_threads = 0
    num_active_threads = 0
    thread_status_dict = {}

    session_ids = get_session_ids.get_session_ids()

    if session_ids is None:
        print "Failed to get session data"
        return None

    def session_needs_worker(s_id):
        return not os.path.isfile('%s%d/working' % (c.CONGRESS_PATH, s_id)) and not os.path.isfile(
            '%s%d/done' % (c.CONGRESS_PATH, s_id))

    for s_id in session_ids:

        if not session_needs_worker(s_id):
            print 'skipping', s_id
            change_num_win_threads(1)
            continue
        while num_active_threads >= c.MAX_ACTIVE_THREADS:
            #    terminalUpdate()
            pass

        change_num_active_threads(1)

        thread.start_new_thread(worker, (s_id,))
        terminalUpdate()

    print 'all workers dispatched. waiting for them to finish'
    prev = num_active_threads
    while num_active_threads > 0:
        # leave terminal open for threads to output to
        if prev == num_active_threads:
            terminalUpdate()
            prev = num_active_threads

    print 'all workers are done. the entire govtrack dataset should now have been mined'
