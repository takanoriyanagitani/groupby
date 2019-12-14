package groupby

import (
  "testing"

  "os"
  "bufio"
)

func TestScan(t *testing.T){
  //tdir := "./.test/GroupBy"
  //e1 := os.MkdirAll(tdir, 0755)
  //switch e1 {
  //  case nil: break
  //  default:  t.Errorf("Unable to create test directory: %v\n", e1)
  //}

  f, e2 := os.Open("../testdata/t1.jsonl")
  switch e2 {
    case nil: break
    default:  t.Errorf("Unable to open test file: %v\n", e2)
  }
  defer f.Close()

  s := bufio.NewScanner(f)

  js := NewJsonReader(s)

  switch js.Scan() { case false: t.Errorf("Unable to get next data.\n") }
  m, e := js.Map()
  switch e {
    case nil: break
    default:  t.Errorf("Unable to get map: %v\n", e)
  }
  switch "google" == m["key"] { case false: t.Errorf("key mismatch.\n") }
  for js.Scan() {
    m, e = js.Map()
    switch nil != e { case true: t.Errorf("Unable to get map: %v\n", e) }
    if "tensorflow" == m["name"] { break }
  }
  switch js.Scan(){ case false: t.Errorf("Unable to get next data.\n") }
  m, e = js.Map()
  switch nil != e { case true: t.Errorf("Unable to get map: %v\n", e) }
  switch "amazon" == m["key"] { case false: t.Errorf("key mismatch.\n") }
  for js.Scan() {
    m, e = js.Map()
    switch nil != e { case true: t.Errorf("Unable to get map: %v\n", e) }
    if "ipad" == m["name"] { break }
  }
  switch js.Scan(){ case false: t.Errorf("Unable to get next data.\n") }
  m, e = js.Map()
  switch e {
    case nil: t.Errorf("No parse error.\n")
    default:  t.Logf("Expected error: %v\n", e)
  }
}
