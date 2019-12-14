import unittest

import app
import os
import operator

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

  pass

def main(): return unittest.main()

def try_exec(): return "__main__" == __name__ and main()

try_exec()
