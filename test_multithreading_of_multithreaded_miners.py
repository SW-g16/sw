# coding=utf-8

import unittest
import namespaces
import time

from db_manager.StardogManager import StardogManager
from mine.MinerManager import MinerManager

import config, test_config

class TestMultiMulti(unittest.TestCase):

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

    def test_mining(self):
        self.miner_manager.mine_all_multithread()

