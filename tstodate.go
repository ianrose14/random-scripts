package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	TimeFormat = "2006-01-02T15:04:05.999999999 MST (-0700)"
)

func main() {
	for _, arg := range os.Args[1:] {
		var t time.Time
		if strings.Index(arg, ".") >= 0 {
			v, err := strconv.ParseFloat(arg, 64)
			if err != nil {
				panic(err)
			}

			nanos := int64(v * float64(time.Second/time.Nanosecond))
			t = time.Unix(0, nanos)
		} else {
			v, err := strconv.ParseInt(arg, 10, 64)
			if err != nil {
				panic(err)
			}

			switch len(arg) {
			case 13:
				// must be milliseconds
				t = time.Unix(0, v*1e6)
			case 16:
				// must be microseconds
				t = time.Unix(0, v*1e3)
			case 19:
				// must be nanoseconds
				t = time.Unix(0, v)
			default:
				// assume it is seconds
				t = time.Unix(v, 0)
			}
		}

		fmt.Println(t.Format(TimeFormat))
		fmt.Println(t.In(time.UTC).Format(TimeFormat))
	}
}
