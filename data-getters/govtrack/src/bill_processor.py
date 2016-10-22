import votes_processor, fsinterface, constants as c

def parse_bill_text(q):
    return '"%s"' % q.replace('"', '').replace('\'', '')


def process_bill(session_id, g, b):
    triples = []

    # if bill reference looks weird, ignore it

    if b[0] != 's' and b[0] != 'h': return []

    # get the individual bills' data from a json file

    bill_data = fsinterface.loadJsonFile('%s%d/votes/%d/%s/data.json' % (c.CONGRESS_PATH, session_id, g, b))

    # if the bill data is no good, ignore it

    if bill_data is None or 'votes' not in bill_data: return []

    # construct bill uri from retrieved bill id

    bill_uri = '<gt_b/%d_%d>' % (session_id, bill_data['number'])

    # add bill text triple

    triples.append((bill_uri, ':hasText', parse_bill_text(bill_data['question'])))

    # bill was processed by either the senate or the house of representatives
    if b[0] == 's':
        triples.append((bill_uri, ':processedBy', '<va/AmericanSenate>'))
    elif b[1] == 'h':
        triples.append((bill_uri, ':processedBy', '<va/AmericanHouseOfRepresentatives>'))

    triples += votes_processor.process_votes(bill_data['votes'], bill_uri)

    return triples
