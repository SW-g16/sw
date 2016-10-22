from pprint import pprint

import govtrack
import time
import process_session

def test_govtrack(empty_threshold,s_id):
    # print 'running test with empty_threshold =',empty_threshold
    session_ids = govtrack.get_session_ids()
    govtrack.wipe_working_tags(session_ids)
    govtrack.wipe_done_tags(session_ids)
    start = time.time()
    process_session.process_session(s_id,empty_threshold)
    return time.time()-start


def find_best_value():

    # ~1500 seems good

    min_ = 750
    interval = 250

    results = []

    best_index = 0
    session_ids_to_test = [n*15 for n in range(1,6)]

    for s in range(0,5):
        results.append([])
        session_id = session_ids_to_test[s]
        for i in range(0,10):
            v = min_+interval*i
            r = test_govtrack(v,session_id)
            results[s].append([v,r])
            print "%d\t%f" % ( v, r )

    averages = []
    test_times = [min_+interval*i for i in range(0,10)]

    for i in range(0,10):
        sum_ = 0
        for j in range(0,len(results)):
            sum_+=results[j][i]
        averages.append(sum_/len(session_ids_to_test))
        print('avg',averages[len(averages)-1])

    return [results,averages]




print test_govtrack(1500,50)
#print find_best_value()

