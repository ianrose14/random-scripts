#!/usr/bin/env python
#
# Script to check whether, in a latex file using the bibitem-\cite reference
# management technique, there are bibliography references that are never cited 
# in the text.  Idea stolen from citations.pl by "SIEi+e, IAC - sinfin [at] iac.es"

import re
import sys

def main():
    args = sys.argv[1:]

    if len(args) == 1:
        bibfile = args[0] + ".bib"
        auxfile = args[0] + ".aux"
    elif len(args) == 2:
        bibfile = args[0]
        auxfile = args[1]
    else:
        print >>sys.stderr, "usage: bibtex-unused.py NAME  -- or -- bibtex-unused.py BIBFILE AUXFILE"
        sys.exit(1)

    cites = set()
    unused = []
    
    pat = re.compile("\s*\\\\bibcite\{([^\}]+)\}")
    aux = open(auxfile, "r")
    
    for line in aux:
        m = pat.match(line)
        if m is not None:
            cites.add(m.group(1))
    aux.close()

    pat = re.compile("\s*@[^\{\(]+[\{\(]([^,]+),")
    bib = open(bibfile, "r")
    usedc = 0
    
    for line in bib:
        m = pat.match(line)
        if m is not None:
            key = m.group(1).strip().lower()
            if key != "string":
                if key not in cites:
                    unused.append(key)
                else:
                    usedc += 1
    bib.close()

    if len(unused) == 0:
        if usedc == len(cites):
            print "%d citations found; all are used!" % usedc
        else:
            print "%d citations found in %s, %d citations found in %s (all used)" % \
                  (len(cites), auxfile, usedc, bibfile)
    else:
        print "%d unused citations found (plus %d used):" % (len(unused), len(cites))
        for key in unused:
            print key

if __name__ == '__main__':
    main()
