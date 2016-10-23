import fsinterface

import constants as c

def get_session_ids():
    candidates = fsinterface.get_int_dirnames(c.CONGRESS_PATH)
    return [i for i in candidates if fsinterface.get_dirnames(c.CONGRESS_PATH+str(i))]