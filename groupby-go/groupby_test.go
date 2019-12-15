package groupby

import (
  "testing"

  "os"
  "bufio"
)

func TestMap(t *testing.T){
  f, e2 := os.Open("../testdata/t1.jsonl")
  switch nil != e2 { case true:  t.Errorf("Unable to open test file: %v\n", e2) }
  defer f.Close()

  s := bufio.NewScanner(f)

  js := NewJsonReader(s)

  switch js.Scan() { case false: t.Errorf("Unable to get next data.\n") }
  m, e := js.Map()
  switch nil != e { case true:  t.Errorf("Unable to get map: %v\n", e) }
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

func TestEquals(t *testing.T){
  a := NewStringKey("apple")
  b := NewStringKey("amazon")
  c := NewStringKey("apple")
  switch a.Equals(b){ case  true: t.Errorf("Not equal.\n") }
  switch c.Equals(a){ case false: t.Errorf("Not differ.\n") }
}
