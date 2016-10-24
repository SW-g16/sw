
def save_dataset(filename, dataset):
    with open(filename, 'w') as f:
        print 'Saving:', filename
        dataset.serialize(f, format='trig')
    print 'Saved.'

