# coding=utf-8

import unittest
import namespaces
import time

from db_manager.StardogManager import StardogManager
from mine.MinerManager import MinerManager

import config, test_config

class TestEachEach(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.db = StardogManager(test_config.TEST_DATABASE_NAME, namespaces.NAMESPACES)
        cls.db.set_up()
        cls.db.data_add(config.ONTOLOGY_PATH)
        cls.miner_manager = MinerManager(cls.db, namespaces, test=test_config.TEST_SIZE)

    @classmethod
    def tearDownClass(cls):

        if test_config.DESTROY_DB_AFTER_TEST:
            cls.db.tear_down()

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print "%s: %.2f" % (self.id(), t)

    def test_parltrack_meps(self):
        self.assertTrue(self.miner_manager.parltrack_miner.__mine_mep_file__())

    def test_parltrack_votes(self):
        self.assertTrue(self.miner_manager.parltrack_miner.__mine_votes_file__())

    def test_parltrack_dossiers(self):
        self.assertTrue(self.miner_manager.parltrack_miner.__mine_dossiers_file__())

    def test_govtrack_bills(self):
        self.assertTrue(self.miner_manager.govtrack_miner.__mine__bills__())

    def test_govtrack_persons(self):
        self.assertTrue(self.miner_manager.govtrack_miner.__mine__persons__())
