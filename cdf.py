#!/usr/bin/env python

from optparse import OptionParser
import math
import sys

def cdf(data, n=100, lessthan=True):
    data = sorted(data)
    fn = float(n)
    vals = []

    if lessthan:
        for i in range(n):
            vals.append(data[int((i+1)*(len(data)-1)/fn)])
    else:
        for i in range(n, 0, -1):
            vals.append(data[int((i)*(len(data)-1)/fn)])
    
    return vals

def main():
    parser = OptionParser(usage="%prog [options] DATA [...]")
    parser.add_option("-n", "--num", action="store", type="int", default=100,
                      help="number of points")
    parser.add_option("-v", "--reverse", action="store_true", default=False,
                      help="reverse fill order")
    parser.add_option("-y", action="store_true", default=False,
                      help="Include y-values")
    (opts, args) = parser.parse_args()
    
    if len(args) == 0:
        data = [float(x) for x in sys.stdin.readlines()]
    else:
        data = [float(x) for x in args]

    vals = cdf(data, n=opts.num, lessthan=(not opts.reverse))
    for i in range(len(vals)):
        if opts.y:
            print vals[i], float(i+1)/opts.num
        else:
            print vals[i]

if __name__ == '__main__':
    main()
