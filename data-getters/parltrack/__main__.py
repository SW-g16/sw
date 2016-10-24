
from rdflib import Dataset
from src import constants as c, main as m, save as s

ds = Dataset()
ds.bind(c.PREFIX, c.ONT)
ds.bind('dbo', c.DBO)
ds.bind('dbr', c.DBR)
ds.bind('dbp', c.DBP)
ds.bind('foaf', c.FOAF)

ds, mep_graph = m.convert_mep(c.DATA_MEP, ds, c.ONT)

ds, dossier_graph = m.convert_dossier(c.DATA_DOSSIER, ds, c.ONT)

ds, votes_graph = m.convert_votes(c.DATA_VOTES, ds, c.ONT)

s.save_dataset(c.DATA_DIR + 'parltrack.trig', ds)
