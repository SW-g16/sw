import os.path

import constants as c
import helpers
import p_votes


def parse_bill_text(q):
    if isinstance(q, basestring):
        return '"%s"' % q.replace('"', '').replace('\'', '')
    elif q is None:
        # this does sometimes occur, such as for session 2 group 2 bill s52
        return "???"
    else:
        print q
        raise Exception


def parse_voting_assembly(b):
    if b[0] == 's':
        return 'dbr:United_States_Senate'
    elif b[0] == 'h':
        return 'dbr:United_States_House_of_Representatives'
    else:
        raise Exception


def process_bill(session_id, g, b):
    # if bill reference looks weird, ignore it
    if b[0] != 's' and b[0] != 'h': return []

    # the path of the bill in the govtrack bulk data directory
    bill_path = '%s%d/votes/%s/%s/data.json' % (c.CONGRESS_PATH, session_id, str(g), b)

    # return 0 triples if there is no data
    if not os.path.isfile(bill_path): return []

    # get the bill's data from a json file
    bill_data = helpers.load_json_file(bill_path)

    # if the bill data is no good, ignore it
    if bill_data is None or 'votes' not in bill_data: return []

    # construct bill uri from retrieved bill id
    bill_uri = '<gt_b/%d_%d>' % (session_id, bill_data['number'])

    # the text of the bill
    bill_text = parse_bill_text(bill_data['question'])

    # the voting assembly that processed the bill (House or Senate)
    voting_assembly = parse_voting_assembly(b)

    # return the processed votes (and abstinations) on the bill
    voting_data = p_votes.process_votes(bill_data['votes'], bill_uri)
    return voting_data + [(bill_uri, ':hasText', bill_text), (bill_uri, ':processedBy', voting_assembly)]
