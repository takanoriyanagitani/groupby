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
