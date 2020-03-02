package main

import (
	"flag"
	"fmt"
	"os"
	"strconv"
	"time"
)

const usage = "usage: dateToTs YEAR MONTH DAY [HOUR [MINUTE [SECOND]]]\n"

func main() {
	utc := flag.Bool("utc", false, "Print in UTC instead of local time")

	args := os.Args[1:]
	if len(args) < 3 || len(args) > 6 {
		fmt.Fprint(os.Stderr, usage)
		os.Exit(2)
	}

	year, err := strconv.Atoi(args[0])
	if err != nil {
		fmt.Fprint(os.Stderr, usage)
		os.Exit(2)
	}

	month, err := strconv.Atoi(args[1])
	if err != nil {
		fmt.Fprint(os.Stderr, usage)
		os.Exit(2)
	}

	day, err := strconv.Atoi(args[2])
	if err != nil {
		fmt.Fprint(os.Stderr, usage)
		os.Exit(2)
	}

	var hours, minutes, seconds int

	if len(args) > 3 {
		hours, err = strconv.Atoi(args[3])
		if err != nil {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
	}

	if len(args) > 4 {
		minutes, err = strconv.Atoi(args[4])
		if err != nil {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
	}

	if len(args) > 5 {
		seconds, err = strconv.Atoi(args[5])
		if err != nil {
			fmt.Fprint(os.Stderr, usage)
			os.Exit(2)
		}
	}

	loc := time.Local
	if *utc {
		loc = time.UTC
	}

	d := time.Date(year, time.Month(month), day, hours, minutes, seconds, 0, loc)
	fmt.Printf("%s  ⇨  %d\n", d.Format(time.RFC3339), d.Unix())
}
