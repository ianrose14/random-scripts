#!/usr/bin/env python

import numpy
import sys

if __name__== '__main__':
    if len(sys.argv) < 2:
        print >>sys.stderr, "usage: stats.py OPERATOR [...ARGS]"
        sys.exit(1)

    op = sys.argv[1]
    args = []
    for arg in sys.argv[2:]:
        try:
            args.append(int(arg))
            continue
        except:
            pass

        try:
            args.append(float(arg))
            continue
        except:
            pass

        args.append(arg)

    try:
        f = getattr(numpy, op)
    except AttributeError:
        print >>sys.stderr, "stats.py: unknown operator"
        sys.exit(1)

    vals = []
    for line in sys.stdin:
        l = line.strip()
        if l != "":
            vals.append(float(l))

    print f(vals, *args)
