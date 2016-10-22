import time

from src import get_session_ids, session_processor, resetdb


def test_session_processor(empty_threshold, s_id):
    session_ids = get_session_ids.get_session_ids()
    resetdb.wipe_working_tags(session_ids)
    resetdb.wipe_done_tags(session_ids)
    start = time.time()
    session_processor.process_session(s_id, empty_threshold)
    return time.time() - start

def find_best_value():
    # ~1500 seems good

    min_ = 750
    interval = 250

    results = []

    session_ids_to_test = [n * 15 for n in range(1, 6)]

    for s in range(0, 5):
        results.append([])
        session_id = session_ids_to_test[s]
        for i in range(0, 10):
            v = min_ + interval * i
            r = test_session_processor(v, session_id)
            results[s].append([v, r])
            print "%d\t%f" % (v, r)

    averages = []

    for i in range(0, 10):
        sum_ = 0
        for j in range(0, len(results)):
            sum_ += results[j][i]
        averages.append(sum_ / len(session_ids_to_test))
        print('avg', averages[len(averages) - 1])

    return [results, averages]


print test_session_processor(1500, 50)
# print find_best_value()
