import json
from itertools import groupby

def parse_json_or_default(j=str(), alt=dict()):
  try:    return json.loads(j)
  except: return alt or {}

def jsonl_groupby(jsonl=iter(list()), row2key=None):
  filtered = filter(lambda line: str == type(line), jsonl)
  parsed   = map(parse_json_or_default, filtered)
  return groupby(parsed, row2key)
