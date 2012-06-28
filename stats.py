#!/usr/bin/env python

import numpy
import sys

if __name__== '__main__':
    if len(sys.argv) != 2:
        print >>sys.stderr, "usage: stats.py OPERATOR"
        sys.exit(1)

    try:
        f = getattr(numpy, sys.argv[1])
    except AttributeError:
        print >>sys.stderr, "stats.py: unknown operator"
        sys.exit(1)

    vals = []
    for line in sys.stdin:
        l = line.strip()
        if l != "":
            vals.append(float(l))

    print f(vals)
