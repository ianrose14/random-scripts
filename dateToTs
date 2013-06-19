#!/usr/bin/env python

import datetime
import sys
import time

def main():
    usage = "dateToTs YEAR MONTH DAY [HOUR [MINUTE [SECOND]]]"
    args = sys.argv[1:]

    if len(args) < 3 or len(args) > 6:
        print >>sys.stderr, usage
        sys.exit(1)

    dt = datetime.datetime(*([int(arg) for arg in args]))
    print int(time.mktime(dt.timetuple()))

if __name__ == '__main__':
    main()
