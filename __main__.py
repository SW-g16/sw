import config
from db_manager.StardogManager import StardogManager
from mine.MinerManager import MinerManager
import namespaces

db = StardogManager(config.DATABASE_NAME, namespaces.NAMESPACES)
db.set_up()
db.data_add(config.ONTOLOGY_PATH)

MinerManager(db, namespaces).mine_all_multithread()