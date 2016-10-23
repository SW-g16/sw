import os
import thread

import time

import session_processor
import get_session_ids

global thread_status_dict
global num_active_threads
global num_win_threads
global num_fail_threads
global init_time
global total_triples

import constants as c

def terminalUpdate():
    print '%d active threads, %d completed threads, %d failed threads' % (
        num_active_threads, num_win_threads, num_fail_threads)


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
    global total_triples

    thread_status_dict[s_id] = 1

    def fail(message):
        print message
        change_num_active_threads(-1)
        change_num_fail_threads(1)
        return False

    def win():
        change_num_active_threads(-1)
        change_num_win_threads(1)
        return True



    # indicate that a worker is already processing this session

    if c.MAX_ACTIVE_THREADS > 1 and mark_session(s_id, 'working') is False: return fail('failed to set work tag %d.' % s_id)

    start = time.time()
    num_triples = session_processor.process_session(s_id)
    total_triples += num_triples
    duration = time.time() - start
    total_duration = time.time()-init_time
    print "%d\t\t%d\t\t%.2f\t\t\t%.2f\t\t\t%d\t\t\t%d\t\t%.2f\t\t\t\t%.2f" % (
            s_id,
          num_triples,

          round(duration,2),
          round(num_triples/duration,2),
          total_duration,

          num_win_threads,
          round(total_duration/max(num_win_threads,0.0001),2),
          round(total_triples/total_duration,2)
    )

    # indicate that a worker has completed processing this session

    if c.MAX_ACTIVE_THREADS > 1 and not mark_session(s_id, 'done'):
        print s_id,'failed after',time.time() - start
        return fail('failed to set done tag %d. ' % s_id)

    # received response from stardog

    thread_status_dict[s_id] = 2

    # return win signal

    return win()


def init(session_ids):

    print '\nsession_id\t' \
          'num_triples\t' \
          'seconds\t\t' \
          'triples_per_second\t' \
          'program run time\t' \
          'num_win_threads\t' \
          'seconds_per_session\t' \
          'average_triples_per_second\t'

    global num_active_threads
    global num_win_threads
    global num_fail_threads
    global thread_status_dict
    global init_time
    global total_triples
    total_triples=0
    init_time = time.time()

    num_fail_threads = 0
    num_win_threads = 0
    num_active_threads = 0
    thread_status_dict = {}

    if session_ids is None:
        print "Failed to get session data"
        return None

    def session_needs_worker(s_id):
        return not os.path.isfile('%s%d/working' % (c.CONGRESS_PATH, s_id)) and not os.path.isfile(
            '%s%d/done' % (c.CONGRESS_PATH, s_id))

    for s_id in session_ids:

        if not session_needs_worker(s_id):
            change_num_win_threads(1)
            continue
        while num_active_threads >= c.MAX_ACTIVE_THREADS:
            #    terminalUpdate()
            pass

        change_num_active_threads(1)
        if c.MAX_ACTIVE_THREADS==1: worker(s_id)
        else: thread.start_new_thread(worker, (s_id,))
        #terminalUpdate()

    print 'all workers dispatched. waiting for them to finish'
    prev = num_active_threads
    while num_active_threads > 0:
        # leave terminal open for threads to output to
        if prev == num_active_threads:
            #terminalUpdate()
            prev = num_active_threads

    print 'all workers are terminated. '
