from rdflib import Dataset
from src import constants as c, main as m, save as s, load_json as h



ds = Dataset()
ds.bind(c.PREFIX, c.ONT)
ds.bind('dbo', c.DBO)
ds.bind('dbr', c.DBR)
ds.bind('dbp', c.DBP)
ds.bind('foaf', c.FOAF)

graph = ds.graph(c.ONT)

ds, graph = m.convert_mep(c.DATA_MEP, ds, graph)

s.save_json(c.DICT_MEPS, m.meps)
s.save_json(c.DICT_PARTIES, m.parties)

ds, graph = m.convert_dossier(c.DATA_DOSSIER, ds, graph)

ds, graph = m.convert_votes(c.DATA_VOTES, ds, graph)

s.save_dataset(c.DATA_OUTPUT, ds)
