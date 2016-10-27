import os.path

import helpers
import p_votes
import constants as c


def parse_bill_text(q):
    if isinstance(q, basestring):
        return '"%s"' % q.replace('"', '').replace('\'', '')
    elif q is None:
        # this does sometimes occur, such as for session 2 group 2 bill s52
        return '"Missing"'
    else:
        print q
        raise Exception


def parse_voting_assembly(b):
    if b[0] == 's':
        return c.URI_USA_SENATE
    elif b[0] == 'h':
        return c.URI_USA_HOUSE
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
    bill_uri = c.PREFIX+':%s_%d_%d' % (b[0],session_id, bill_data['number'])

    # the text of the bill
    bill_text = parse_bill_text(bill_data['question'])

    # the voting assembly that processed the bill (House or Senate)
    voting_assembly = parse_voting_assembly(b)

    # return the processed votes (and abstinations) on the bill
    voting_data = p_votes.process_votes(bill_data['votes'], bill_uri)
    return voting_data + [(bill_uri, c.PROP_BILL_TEXT, bill_text), (bill_uri, c.PROP_PROCESSED_BY, voting_assembly)]
