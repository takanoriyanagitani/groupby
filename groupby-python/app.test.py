import unittest

import app

class T1(unittest.TestCase):
  def test_parse_json_or_default(self):
    self.assertEqual({}, app.parse_json_or_default())
    self.assertEqual({}, app.parse_json_or_default("{}"))
    self.assertEqual({}, app.parse_json_or_default("{"))
    self.assertEqual({}, app.parse_json_or_default("["))
    self.assertEqual({"id": "some id"}, app.parse_json_or_default('{"id": "some id"}'))
    self.assertEqual({"id": "some id", "unixtime": 1500299792458}, app.parse_json_or_default('{"id": "some id", "unixtime": 1500299792458}'))
    pass
  pass

def main(): return unittest.main()

def try_exec(): return "__main__" == __name__ and main()

try_exec()
