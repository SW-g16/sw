
import helpers as h

import constants as c

def get_session_ids():
    candidates = h.get_int_dirnames(c.CONGRESS_PATH)
    return sorted([i for i in candidates if h.get_dirnames(c.CONGRESS_PATH + str(i))],reverse=True)
