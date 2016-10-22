import fsinterface

import constants as c

def get_session_ids():
    return fsinterface.get_int_dirnames(c.CONGRESS_PATH)
