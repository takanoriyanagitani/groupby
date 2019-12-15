package groupby

import (
  "bufio"
  "encoding/json"
)

type JsonlScanner struct {
  s *bufio.Scanner
}

func NewJsonReader(s *bufio.Scanner) *JsonlScanner { return &JsonlScanner{ s: s } }

func (j *JsonlScanner) Scan() bool { return j.s.Scan() }

func (j *JsonlScanner) Map() (map[string]interface{}, error) {
  b := j.s.Bytes()
  m := make(map[string]interface{})
  e := json.Unmarshal(b, &m)
  return m, e
}

type Key interface {
  Equals(other Key)
}

type StringKey struct { s string }

func NewStringKey(s string) *StringKey { return &StringKey{ s: s } }

func (a *StringKey) Equals(b *StringKey) bool { return a.s == b.s }

type MapKey struct { m map[string]Key }

func (a *MapKey) Equals(b *MapKey) bool {
  switch len(a.m) != len(b.m) { case true: return false }
  for key, value := range a.m {
    switch value != b.m[key] { case true: return false }
  }
  return true
}
