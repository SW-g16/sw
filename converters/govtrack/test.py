import govtrack


def test_govtrack():
    session_ids = govtrack.get_session_ids()
    govtrack.wipe_working_tags(session_ids)
    govtrack.wipe_done_tags(session_ids)
    print 'Session_45:', govtrack.process_session(45) == True


test_govtrack()
