import ijson

from Miner import Miner
import subprocess
import os
from multiprocessing.dummy import Pool as ThreadPool


NAME_KEYS = ('sur', 'family')

class ParlTrackMiner(Miner):

    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    DL_DIR = '%s/s' % DIR_PATH

    __get_filestream__ = lambda self , key : open('%s/%s.json' % (self.DL_DIR,key),'r')


    timeformat = lambda _, t : '"%s"^^xsd:date' % t.split('T')[0] #'"%s"' % strptime(t.split('T')[0], '%Y-%m-%d')


    def __init__(self, db, namespaces, test=False):
        super(ParlTrackMiner, self).__init__(db, namespaces, test)


    def mine(self):
        if not os.path.isdir(self.DL_DIR): os.mkdir(self.DL_DIR)
        subprocess.call('bash %s/parltrack_download.sh %s' % (self.DIR_PATH, self.DL_DIR), shell=True)
        res = ThreadPool(3).map(lambda x:x(), [self.__mine_mep_file__,self.__mine_dossiers_file__,self.__mine_votes_file__])
        print 'Parltrack done with mining'
        return res

    def __mine_mep_file__(self):

        filestream = self.__get_filestream__('meps')

        # the names are sometimes in an odd format, such as the last name being in all upper-case
        # we don't know their preferred capitalizations, but hope they don't mind "Firstname Lastname"
        nameformat = lambda x: ' '.join([s[0].upper()+(s[1:].lower() if len(s)>1 else '') for s in ' '.join([x[k] for k in NAME_KEYS if k in x]).strip().replace('  ',' ').split(' ')])

        iterations = 0

        # using ijson to stream the very large files, instead of loading the whole json file at once, which caused OS crashes
        for mep in ijson.items(filestream, 'item'):

            if self.test:
                iterations += 1
                if iterations > self.test:
                    return True

            # unique_identifier = mep['UserID']
            # this is a unique url which we could use as the uri. It includes the unique identifier,
            # and can be constructed from just the unique identifier (http://www.europarl.europa.eu/meps/en/<unique_identifier>/_history.html)
            # it has an ugly /_history.html suffix which is necessary for accessing the browser page
            profile_link = '<%s>' % mep['meta']['url']

            # we decide to use the profile link as URI
            mep_uri = profile_link

            # and keep the unique id as well. perhaps redundant, since it can be extracted from the profile link/uri
            #self.add_triple('%s votes:parltrack_id %s.' % (mep_uri, mep['UserID']))

            # the MEP is a member of the EU parliament
            self.add_triple('%s <%s> <%s>.' % (mep_uri, self.namespaces.OFFICE, self.namespaces.MEMBER_OF_EU))

            self.add_triple('%s foaf:name "%s".' % (mep_uri, nameformat(mep['Name'])))

            # some meps have a link to a photo
            if 'Photo' in mep:
                self.add_triple('%s <%s> <%s>.' % (mep_uri, self.namespaces.THUMBNAIL, mep['Photo']))

            if 'Birth' in mep:
                if 'date' in mep['Birth']:
                    self.add_triple('%s <%s> %s.' % (mep_uri, self.namespaces.BIRTH_DATE, self.timeformat(mep['Birth']['date'])))
                if 'place' in mep['Birth']:
                    self.add_triple('%s <%s> "%s".' % (mep_uri, self.namespaces.BIRTH_PLACE, mep['Birth']['place']))

            if 'Death' in mep:
                self.add_triple('%s <%s> %s.' % (mep_uri,self.namespaces.DEATH_DATE,self.timeformat(mep['Death'])))

            if 'Gender' in mep:
                assert mep['Gender'] in ['M','F']
                self.add_triple('%s foaf:gender "%s".' % (mep_uri, mep['Gender']))

            # see comment on this in party-issue.md



            if 'Groups' in mep:
                for group in mep['Groups']:

                    # no link is given, so we construct a uri from the uniquely identifying groupid field
                    # there are sometimes multiple id's. in those cases, we naively use the first listed

                    party_uri = 'http://parltrack.euwiki.org/party/%s' % (group['groupid'][0] if isinstance(group['groupid'],list) else group['groupid'])

                    party_name = group['Organization']

                    # party association period available in party_data['start'], party_data['end']

                    self.add_triple('<%s> votes:party_name "%s".' % (party_uri, party_name))
                    self.add_triple('%s votes:party <%s>.' % (mep_uri, party_uri))

                    self.add_triple('%s <%s> <%s>.' % (mep_uri, self.namespaces.PARTY, party_uri))
                    self.add_triple('<%s> <%s> <%s>.' % (party_uri, self.namespaces.IN_LEGISLATURE, self.namespaces.EUROPEAN_PARLIAMENT))

        self.add_to_db(self.triples)
        print 'Parltrack done mining representatives'
        return True


    def __mine_dossiers_file__(self):

        filestream = self.__get_filestream__('dossiers')

        iterations = 0

        # using ijson to stream the very large files, instead of loading the whole json file at once, which caused OS crashes
        for dossier in ijson.items(filestream, 'item'):


            if self.test:
                iterations += 1
                if iterations > self.test:
                    break

            if not '_id' in dossier:
                # can't construct uri, can't attach any other data to anything
                continue

            # we construct a URI from a unique integer. this address doesn't exist outsite of this context
            dossier_uri = '<http://parltrack.euwiki.org/dossier/%s>' % dossier['_id']
            self.add_triple('%s <%s> <%s>.' % (dossier_uri,self.namespaces.PROCESSED_BY,self.namespaces.EUROPEAN_PARLIAMENT))

            if 'activities' in dossier and len(dossier['activities'])>0 and 'date' in dossier['activities'][0]:
                dossier_date = self.timeformat(dossier['activities'][0]['date'])
                self.add_triple('%s <%s> %s.' % (dossier_uri,self.namespaces.DATE,dossier_date))

            if 'procedure' in dossier and 'title' in dossier['procedure']:
                dossier_title = dossier['procedure']['title']
                self.add_triple('%s <%s> "%s".' % (dossier_uri,self.namespaces.DOSSIER_TITLE,dossier_title.replace('"','\'')))



        self.add_to_db(self.triples)
        print 'Parltrack done mining dossiers'
        return True

    def __mine_votes_file__(self):

        filestream = self.__get_filestream__('votes')

        direction_verb_map = {
            'Abstain':self.namespaces.ABSTAINS,
            'For':self.namespaces.VOTES_FOR,
            'Against':self.namespaces.VOTES_AGAINST
        }
        iterations = 0
        for votes in ijson.items(filestream, 'item'):

            if self.test:
                iterations += 1
                if iterations > self.test:
                    break

            if 'dossierid' not in votes: continue

            dossier_uri = 'http://parltrack.euwiki.org/dossier/%s' % votes['dossierid']
            for direction in ['Abstain','For','Against']:
                if direction not in votes or 'groups' not in votes[direction]: continue
                for group in votes[direction]['groups']:
                    if 'votes' not in group: continue
                    for vote in group['votes']:
                        if 'ep_id' not in vote: continue
                        self.add_triple(
                            '<%s> <%s> <%s>.' % (
                                'http://www.europarl.europa.eu/meps/en/%s/_history.html' % vote['ep_id'],
                                direction_verb_map[direction],
                                dossier_uri
                            )
                        )

        self.add_to_db(self.triples)
        print 'Parltrack done mining votes'
        return True