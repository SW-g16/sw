import time

from src import p_session, p_bill, p_votes


def reset_db():
    from subprocess import call
    call(["sh", "sw/scripts/reset-db.sh"])


def test_votes_processor(votes, bill_uri):
    start = time.time()
    print p_votes.process_votes(votes, bill_uri)
    return time.time() - start


def test_bill_processor(s_id, g, b_id):
    start = time.time()
    print p_bill.process_bill(s_id, g, b_id)
    return time.time() - start


def test_session_processor(s_id):
    start = time.time()
    p_session.process_session(s_id)
    return time.time() - start


reset_db()

print test_votes_processor({'Yea': [{'id': 'test_voter'}, {'id': 'other_test_voter'}],
                            'Nay': [{'id': 'test_voter_2'}, {'id': 'other_test_voter_2'}],
                            'Not Voting': [{'id': 'test_voter_3'}, {'id': 'other_test_voter_3'}]}, "<test_bill>")

reset_db()

print test_bill_processor(3, 1, 's3')

reset_db()

print test_session_processor(16)

reset_db()
