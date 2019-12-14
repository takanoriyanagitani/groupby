import json
from itertools import groupby

def parse_json(j=bytes(), alt=dict()):
  try:    return (True,  j, json.loads(j.decode("utf-8")))
  except: return (False, j, alt                          )

def jsonl_groupby(jsonl=iter(list()), f=None, row2key=None):
  filtered = filter(lambda line: str == type(line), jsonl)
  parsed   = map(parse_json_or_default, filtered)
  return groupby(filter(f, parsed), row2key)
