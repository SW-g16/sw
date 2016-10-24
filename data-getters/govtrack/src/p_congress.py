import time
from pprint import pprint

import p_session


def print_result_table_headers():
    print "s_id\tnum_triples\tprocessing_time\tstardog_wait_time\ttriples_per_second"


def print_result_row(s_id, result_row):
    print "%d\t%d\t\t%0.2f\t\t%0.2f\t\t\t%0.2f" % (
        s_id, result_row['num_triples'], round(result_row['processing_time'], 2),
        round(result_row['stardog_wait_time'], 2), round(result_row['num_triples'] / result_row['processing_time'], 2))


def process_congress(session_ids):
    init_time = time.time()

    report = {'session_reports': {}, 'total_num_triples': 0, 'total_processing_time': 0}

    if session_ids is None or not all(isinstance(item, int) for item in session_ids):
        raise ValueError("The provided session ids were not all integers: ", session_ids)

    print_result_table_headers()

    for s_id in [3]:
        report['session_reports'][s_id] = p_session.process_session(s_id)
        print_result_row(s_id, report['session_reports'][s_id])

    report['total_processing_time'] = time.time() - init_time
    report['total_num_triples'] = sum([report['session_reports'][i]['num_triples'] for i in report['session_reports']])
    report['average_triples_per_second'] = report['total_num_triples'] / report['total_processing_time']

    print 'Done :) dumping report below.'

    pprint(report)
