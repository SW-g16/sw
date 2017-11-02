
from multiprocessing.pool import ThreadPool

from mine.GovTrackMiner import GovTrackMiner
from mine.ParlTrackMiner import ParlTrackMiner


class MinerManager(object):

    def __init__(self, db, namespaces, test=False):
        self.govtrack_miner = GovTrackMiner(db, namespaces, test)
        self.parltrack_miner = ParlTrackMiner(db, namespaces, test)
        if test: print 'Mining test with test=%s' % test

    def mine_all_multithread(self): return ThreadPool(2).map(lambda x:x(), [self.govtrack_miner.mine,self.parltrack_miner.mine])
    def mine_parltrack(self):self.parltrack_miner.mine()
    def mine_govtrack(self):self.govtrack_miner.mine()