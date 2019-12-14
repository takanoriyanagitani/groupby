import unittest

import app
import os
import operator
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

  pass

def main(): return unittest.main()

def try_exec(): return "__main__" == __name__ and main()

try_exec()
