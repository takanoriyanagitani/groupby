import json
import os
import operator
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

def jsonl_group2file(key, it, key2filename):
  filename = key2filename(key)
  dname = os.path.dirname(filename)
  os.makedirs(dname, exist_ok=True)
  tname = filename + ".temp"
  with open(tname, mode="wb") as f:
    filtered = filter(lambda t: tuple == type(t) and 3 == len(t) and bytes == type(t[1]), it)
    mapped   = map(operator.itemgetter(1), filtered)
    for b in mapped: f.write(b)
    f.flush()
    os.fdatasync(f.fileno())
    pass
  os.rename(tname, filename)
  pass
