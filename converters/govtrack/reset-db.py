
import govtrack

def clean():
    session_ids = govtrack.get_session_ids()
    govtrack.wipe_working_tags(session_ids)
    govtrack.wipe_done_tags(session_ids)
    from subprocess import call
    call(["sh", "sw/scripts/other/reset-db.sh"])

clean()