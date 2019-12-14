import json
from itertools import groupby

def parse_json(j=bytes(), alt=dict()):
  try:    return (True,  j, json.loads(j.decode("utf-8")))
  except: return (False, j, alt                          )

def jsonl2tups(jsonl=iter(list())):
  filtered = filter(lambda line: bytes == type(line), jsonl)
  return map(parse_json, filtered)

def jsonl_groupby(jsonl=iter(list()), f=None, row2key=None):
  tups = jsonl2tups(jsonl)
  return groupby(filter(f, tups), row2key)
