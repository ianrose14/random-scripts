#!/usr/bin/env python

import sys

ANSI_CODES = { 'reset': 0,
               'bold': 1,
               'dim': 2,
               'italics': 3,
               'underline': 4,
               'blink': 5,
               'reverse': 7,
               'hidden': 8,
               'strikethrough': 9,
               'bold_off': 22,
               'italics_off': 23,
               'underline_off': 24,
               'inverse_off': 27,
               'strikethrough_off': 29,
               'black': 30,
               'red': 31,
               'green': 32,
               'yellow': 33,
               'blue': 34,
               'magenta': 35,
               'cyan': 36,
               'white': 37,
               'reset' : 39,
               'black bg': 40,
               'red bg': 41,
               'green bg': 42,
               'yellow bg': 43,
               'blue bg': 44,
               'magenta bg': 45,
               'cyan bg': 46,
               'white bg': 47,
               'reset bg': 49 }

# copied from http://code.activestate.com/recipes/475186/
# I'm not 100% sure that this works correctly in the general case (what if you
# created multiple terminals?  How does curses know which one you are referring
# to?), but it seems to work find for typical usage.
def has_colors(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False

def format(text, codes=[], fd=sys.stdout, reset=True, force=False):
    if not force:
        if not has_colors(fd):
            return text
    strs = [ chr(27) + "[0" ]
    for code in codes:
        strs.append(";%d" % ANSI_CODES[code])
    strs.append("m%s" % text)
    if reset:
        strs.append(chr(27) + "[0m")
    return ''.join(strs)

def setfont(codes=[], fd=sys.stdout, force=False):
    """Equivalent to:
    fd.write(format("", codes, fd, True, force))
    """
    fd.write(format("", codes=code, fd=fd, reset=False, force=force))

def write(text, codes=[], fd=sys.stdout, force=False):
    """Equivalent to:
    fd.write(format(text, codes, fd, force))
    """
    fd.write(format(text, codes=codes, fd=fd, reset=True, force=force))

if __name__ == '__main__':
    write("this is a red and bold test\n", ['red', 'bold'])
    write("this is a ")
    write("cyan", ['cyan', 'underline'])
    write(" and ")
    write("yellow on blue", ['yellow', 'blue bg'])
    write(" test\n")
    print "here is an", format("ugly test with format()", ['magenta', 'white bg', 'italics'])
    print "this is a", format("forced test", ['blue', 'bold'], force=True)
    print "this is a", format("spillover test", ['red'], reset=False)
    print "this line specifies no formatting"
    write("this is a codes=[] write\n", codes=[])
    print "the end!"
