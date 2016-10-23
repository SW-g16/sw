import votes_processor, fsinterface, constants as c
import os.path

def parse_bill_text(q):
    if q is None : return False
    return '"%s"' % q.replace('"', '').replace('\'', '')


def parse_voting_assembly(b):
    # bill was processed by either the senate or the house of representatives
    return '<va/AmericanSenate>' if b[0] == 's' else '<va/AmericanHouseOfRepresentatives>'


def process_bill(session_id, g, b):

    # if bill reference looks weird, ignore it
    if b[0] != 's' and b[0] != 'h': return []

    bill_path = '%s%d/votes/%d/%s/data.json' % (c.CONGRESS_PATH, session_id, g, b)

    if not os.path.isfile(bill_path): return []

    # get the individual bills' data from a json file
    bill_data = fsinterface.loadJsonFile(bill_path)

    # if the bill data is no good, ignore it
    if bill_data is None or 'votes' not in bill_data: return []

    # construct bill uri from retrieved bill id
    bill_uri = '<gt_b/%d_%d>' % (session_id, bill_data['number'])

    return [
        (bill_uri, ':hasText', parse_bill_text(bill_data['question'])),
        (bill_uri, ':processedBy', parse_voting_assembly(b))
    ] + votes_processor.process_votes(bill_data['votes'], bill_uri)
