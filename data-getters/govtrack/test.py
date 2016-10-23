import time

from src import session_processor, resetdb, bill_processor, votes_processor

def test_votes_processor(votes, bill_uri):
    resetdb.clean()
    start = time.time()
    print votes_processor.process_votes(votes,bill_uri)
    return time.time() - start

def test_bill_processor(s_id,g,b_id):
    resetdb.clean()
    start = time.time()
    print bill_processor.process_bill(s_id,g,b_id)
    return time.time() - start

def test_session_processor(s_id):
    start = time.time()
    session_processor.process_session(s_id)
    return time.time() - start

#print test_votes_processor({'Yea':[{'id':'test_voter'},{'id':'other_test_voter'}],'Nay':[{'id':'test_voter_2'},{'id':'other_test_voter_2'}],'Not Voting':[{'id':'test_voter_3'},{'id':'other_test_voter_3'}] },"<test_bill>")

#print test_bill_processor(3,1,'s3')
"""
TEST_SESSION_ID = 14
for threshold in [1000,2000,3000] :
    print threshold, test_session_processor(TEST_SESSION_ID,threshold)
"""

resetdb.clean()

for i in range(10,40):
    print i,test_session_processor(i)