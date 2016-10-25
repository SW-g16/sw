from rdflib import Dataset
from src import constants as c, main as m, save as s, load_json as h

ds = Dataset()
ds.bind(c.PREFIX, c.ONT)
ds.bind('dbo', c.DBO)
ds.bind('dbr', c.DBR)
ds.bind('dbp', c.DBP)
ds.bind('foaf', c.FOAF)

graph = ds.graph(c.ONT)

mep_data = h.load_json(c.DATA_MEP)
ds, graph = m.convert_mep(mep_data, ds, graph)

s.save_json(c.DICT_MEPS, m.dict_mep)
s.save_json(c.DICT_PARTIES, m.dict_party)

dossier_data = h.load_json(c.DATA_DOSSIER)
ds, graph = m.convert_dossier(dossier_data, ds, graph)

votes_data = h.load_json(c.DATA_VOTES)
ds, graph = m.convert_votes(votes_data, ds, graph)

s.save_dataset(c.DATA_OUTPUT, ds)
