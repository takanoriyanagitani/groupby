import unittest

import app
import os
import operator
import json
from itertools import zip_longest

class T1(unittest.TestCase):
  def test_parse_json_or_default(self):
    self.assertEqual((False, bytes(), {}), app.parse_json())
    self.assertEqual((False, bytes(), {}), app.parse_json(b""))
    self.assertEqual((False, b"{",    {}), app.parse_json(b"{"))
    self.assertEqual((False, b"}",    {}), app.parse_json(b"}"))
    self.assertEqual((False, b"]",    {}), app.parse_json(b"]"))
    self.assertEqual((False, b"[",    {}), app.parse_json(b"["))
    self.assertEqual((True,  b"{}",   {}), app.parse_json(b"{}"))
    pass

  def test_jsonl2tups(self):
    i = iter([
      b'{"key": "america", "unixtime": 0, "name": "canada"}',
      b'{"key": "america", "unixtime": 0, "name": "united states"}',
      b'{"key": "asia",    "unixtime": 0, "name": "china"}',
      b'{"key": "asia",    "unixtime": 0, "name": "japan"}',
      b'{"key": "asia",    "unixtime": 0, "name": "korea"}',
      b'{"key": "america", "unixtime": 0, "name": "new york"}',
      b'{"key": "asia",    "unixtime": 0, "name": "tokyo"}',
      b'{parse err sample',
      b' parse err sample]',
      b'{"key": "asia",    "unixtime": 0, "name": "yokohama"}',
    ])
    a = app.jsonl2tups(i)
    e = [
      ( True, b'{"key": "america", "unixtime": 0, "name": "canada"}',        {"key": "america", "unixtime": 0, "name": "canada"       }),
      ( True, b'{"key": "america", "unixtime": 0, "name": "united states"}', {"key": "america", "unixtime": 0, "name": "united states"}),
      ( True, b'{"key": "asia",    "unixtime": 0, "name": "china"}',         {"key": "asia",    "unixtime": 0, "name": "china"        }),
      ( True, b'{"key": "asia",    "unixtime": 0, "name": "japan"}',         {"key": "asia",    "unixtime": 0, "name": "japan"        }),
      ( True, b'{"key": "asia",    "unixtime": 0, "name": "korea"}',         {"key": "asia",    "unixtime": 0, "name": "korea"        }),
      ( True, b'{"key": "america", "unixtime": 0, "name": "new york"}',      {"key": "america", "unixtime": 0, "name": "new york"     }),
      ( True, b'{"key": "asia",    "unixtime": 0, "name": "tokyo"}',         {"key": "asia",    "unixtime": 0, "name": "tokyo"        }),
      (False, b'{parse err sample',                                          {                                                        }),
      (False, b' parse err sample]',                                         {                                                        }),
      ( True, b'{"key": "asia",    "unixtime": 0, "name": "yokohama"}',      {"key": "asia",    "unixtime": 0, "name": "yokohama"     }),
    ]
    z = zip_longest(a, e)
    for t in z:
      ta = t[0]
      te = t[1]
      self.assertEqual(ta[0], te[0])
      self.assertEqual(ta[1], te[1])
      self.assertEqual(ta[2], te[2])
    pass

  def test_jsonl_groupby(self):
    i = iter([
      b'{"key": "solid",  "unixtime": 0, "name": "c" }',
      b'{"key": "solid",  "unixtime": 1, "name": "al"}',
      b'{"key": "liquid", "unixtime": 0, "name": "hg"}',
      b'{"key": "liquid", "unixtime": 1, "name": "br"}',
      b'{"key": "gas",    "unixtime": 0, "name": "he"}',
      b'{"key": "gas",    "unixtime": 1, "name": "ne"}',
      b'{"key": "solid",  "unixtime": 2, "name": "au"}',
      b'{"key": "solid",  "unixtime": 3, "name": "ag"}',
    ])
    f = lambda t: tuple == type(t) and 3 == len(t) and bool == type(t[0]) and t[0] and dict == type(t[2]) and "key" in t[2]
    row2key = lambda t: t[2]["key"]
    a = app.jsonl_groupby(i, f, row2key)
    e = iter([
      ("solid", iter([
        (True, b'{"key": "solid",  "unixtime": 0, "name": "c" }', {"key": "solid", "unixtime": 0, "name": "c"}),
        (True, b'{"key": "solid",  "unixtime": 1, "name": "al"}', {"key": "solid", "unixtime": 1, "name": "al"}),
      ])),
      ("liquid", iter([
        (True, b'{"key": "liquid", "unixtime": 0, "name": "hg"}', {"key": "liquid", "unixtime": 0, "name": "hg"}),
        (True, b'{"key": "liquid", "unixtime": 1, "name": "br"}', {"key": "liquid", "unixtime": 1, "name": "br"}),
      ])),
      ("gas", iter([
        (True, b'{"key": "gas",    "unixtime": 0, "name": "he"}', {"key": "gas", "unixtime": 0, "name": "he"}),
        (True, b'{"key": "gas",    "unixtime": 1, "name": "ne"}', {"key": "gas", "unixtime": 1, "name": "ne"}),
      ])),
      ("solid", iter([
        (True, b'{"key": "solid",  "unixtime": 2, "name": "au"}', {"key": "solid", "unixtime": 2, "name": "au"}),
        (True, b'{"key": "solid",  "unixtime": 3, "name": "ag"}', {"key": "solid", "unixtime": 3, "name": "ag"}),
      ])),
    ])
    z = zip_longest(a, e)
    for t in z:
      ta = t[0]
      te = t[1]
      self.assertEqual(tuple, type(ta))
      self.assertEqual(tuple, type(te))
      self.assertEqual(2, len(ta))
      self.assertEqual(2, len(te))
      ka = ta[0]
      ke = te[0]
      self.assertEqual(str, type(ka))
      self.assertEqual(ka, ke)
      ia = ta[1]
      ie = te[1]
      for it in zip_longest(ia, ie):
        self.assertEqual(tuple, type(it[0]))
        self.assertEqual(tuple, type(it[1]))
        self.assertEqual(3, len(it[0]))
        self.assertEqual(3, len(it[1]))
        self.assertEqual(it[0][0], it[1][0])
        self.assertEqual(it[0][1], it[1][1])
        self.assertEqual(it[0][2], it[1][2])
        pass
      pass
    pass

  def test_jsonl_group2file(self):
    tdir = "./.test/jsonl_group2file"
    os.makedirs(tdir, exist_ok=True)
    f = lambda t: tuple == type(t) and 3 == len(t) and bool == type(t[0]) and t[0] and dict == type(t[2]) and "key" in t[2]
    row2key = lambda t: t[2]["key"]
    key2filename = lambda key: os.path.join(tdir, key + ".jsonl")
    jname = "../testdata/t1.jsonl"
    self.assertTrue(os.path.isfile(jname))
    with open(jname, mode="rb") as j:
      g = app.jsonl_groupby(j, f, row2key)
      for key, it in g: app.jsonl_group2file(key, it, key2filename)
      self.assertTrue(os.path.isfile(os.path.join(tdir, "google.jsonl")))
      self.assertTrue(os.path.isfile(os.path.join(tdir, "amazon.jsonl")))
      self.assertTrue(os.path.isfile(os.path.join(tdir, "facebook.jsonl")))
      self.assertTrue(os.path.isfile(os.path.join(tdir, "apple.jsonl")))
      with open(os.path.join(tdir, "google.jsonl"), mode="rb") as g:
        a = map(lambda b: json.loads(b.decode("utf-8")), g)
        e = [
          {"key": "google",   "unixtime": 0, "name": "search"    },
          {"key": "google",   "unixtime": 1, "name": "android"   },
          {"key": "google",   "unixtime": 2, "name": "tensorflow"},
        ]
        self.assertEqual(e, list(a))
      with open(os.path.join(tdir, "amazon.jsonl"), mode="rb") as a:
        a = map(lambda b: json.loads(b.decode("utf-8")), a)
        e = [
          {"key": "amazon",   "unixtime": 0, "name": "shop"      },
          {"key": "amazon",   "unixtime": 1, "name": "kindle"    },
          {"key": "amazon",   "unixtime": 2, "name": "aws"       },
        ]
        self.assertEqual(e, list(a))
      with open(os.path.join(tdir, "facebook.jsonl"), mode="rb") as f:
        a = map(lambda b: json.loads(b.decode("utf-8")), f)
        e = [
          {"key": "facebook", "unixtime": 0, "name": "sns"       },
          {"key": "facebook", "unixtime": 1, "name": "react"     },
          {"key": "facebook", "unixtime": 2, "name": "pytorch"   },
        ]
        self.assertEqual(e, list(a))
      with open(os.path.join(tdir, "apple.jsonl"), mode="rb") as a:
        a = map(lambda b: json.loads(b.decode("utf-8")), a)
        e = [
          {"key": "apple",    "unixtime": 0, "name": "mac"       },
          {"key": "apple",    "unixtime": 1, "name": "iphone"    },
          {"key": "apple",    "unixtime": 2, "name": "ipad"      },
          {"key": "apple",    "unixtime": 3, "name": "tv"        },
          {"key": "apple",    "unixtime": 4, "name": "app"       },
        ]
        self.assertEqual(e, list(a))
      pass
    pass

  pass

def main(): return unittest.main()

def try_exec(): return "__main__" == __name__ and main()

try_exec()
