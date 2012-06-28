#!/usr/bin/env python

import ansi
import os
import sys
import textwrap
import types

class TableFormat:
    def __init__(self, ncolumns, sepstr="", tablewidth=None):
        if tablewidth is None:
            if 'COLUMNS' in os.environ:
                tablewidth = int(os.environ['COLUMNS'])
            else:
                tablewidth = 80

        self.sepstr = sepstr
        self.ncolumns = ncolumns
        self.colwidth = tablewidth/ncolumns - len(sepstr)  # leave space for border
        self.tablewidth = (self.colwidth + len(sepstr))*ncolumns - len(sepstr)
        self.colbufs = []
        
        for i in range(ncolumns):
            self.colbufs.append([])
        
    def newrow(self):
        """Advance to new row of the table; sorta like a carriage return"""
        maxlen = 0
        for colbuf in self.colbufs:
            maxlen = max(maxlen, len(colbuf))

        for i in range(maxlen):
            first = True
            for colbuf in self.colbufs:
                if first:
                    first = False
                else:
                    sys.stdout.write(self.sepstr)
                if i < len(colbuf):
                    sys.stdout.write(colbuf[i])
                else:
                    sys.stdout.write(" "*self.colwidth)
            sys.stdout.write("\n")

        self.colbufs = []
        for i in range(self.ncolumns):
            self.colbufs.append([])

    def writecol(self, index, text, ansicodes=[], wrap=True, border=False, center=False, padding=(0,0,0,0)):
        self.colbufs[index] = []
        ansistart = ansi.format("", ansicodes, reset=False)
        ansistop = ansi.format("", ["reset"], reset=False)

        if border:
            width = self.colwidth - 4 - padding[2] - padding[3]
        else:
            width = self.colwidth - padding[2] - padding[3]

        lines = []

        for i in range(padding[0]):
            # prevent ansi formatting from covering blank spaces
            lines.append(ansistop + " "*width + ansistart)

        if type(text) == types.StringType:
            text = [ text ]
            
        for textline in text:
            extra = width - len(textline)
            if extra >= 0:
                if center:
                    # prevent ansi formatting from covering blank spaces
                    lines.append(ansistop + " "*(extra/2) + ansistart + textline +
                                 ansistop + (" "*(extra - (extra/2))) + ansistart)
                else:
                    # prevent ansi formatting from covering blank spaces
                    lines.append(textline + ansistop + " "*extra + ansistart)
            elif wrap:
                for line in textwrap.TextWrapper(width=width).wrap(textline):
                    lines.append(line.ljust(width))
            else:
                # truncate text
                lines.append(textline[:width])
            
        for i in range(padding[1]):
            # prevent ansi formatting from covering blank spaces
            lines.append(ansistop + " "*width + ansistart)
        
        if border:
            if type(border) == types.StringType:
                if len(border) > 1:
                    raise ValueError("border must be either a boolean or a single character")
                horiz = ansistart + " " + border*(self.colwidth-2) + " " + ansistop
                sidechar = border
            elif type(border) != types.BooleanType:
                raise ValueError("border must be either a boolean or a single character")
            else:
                # border == True, use default characters
                horiz = ansistart + " " + "-"*(self.colwidth-2) + " " + ansistop
                sidechar = "|"

            # put the padding INSIDE the side-border (which, in turn, is inside
            # the ansi codes)
            prefix = ansistart + sidechar + " " + " "*padding[2]
            suffix = " "*padding[3] + " "  + sidechar + ansistop
        else:
            # put the padding OUTSIDE the ansi codes
            prefix = " "*padding[2] + ansistart
            suffix = ansistop + " "*padding[3]

        if border: self.colbufs[index].append(horiz)
        for line in lines:
            self.colbufs[index].append(prefix + line + suffix)
        if border: self.colbufs[index].append(horiz)

    def writeline(self, char="-"):
        self.newrow()
        self.writefullrow(char*self.tablewidth)
        self.newrow()

    def writefullcol(self, index, fillchar=' '):
        self.writecol(index, fillchar*self.colwidth)

    def writefullrow(self, text):
        self.newrow()
        sys.stdout.write(text[:self.tablewidth])
        sys.stdout.write("\n")
        self.newrow()

def main():
    for i in range(4):
        print
        if i == 0:
            print ">>> first a table with cell lines"
            table = TableFormat(5, " | ", 100)
            border = False
        elif i == 1:
            print ">>> now a table with cell boxes"
            table = TableFormat(5, "", 100)
            border = True
        elif i == 2:
            print ">>> now a table with custom (star) boxes"
            table = TableFormat(5, "", 100)
            border = "*"
        elif i == 3:
            print ">>> now a table that will fail with a bad border"
            table = TableFormat(5, "", 100)
            border = "toolong"
        print
        
        table.writeline()
        table.writefullrow("hey man this is the table title row")
        table.writeline()
        table.writefullrow("hey man this is what the table title row would have looked like if I had made it really long")
        table.writeline()
        for i in range(5):
            table.writecol(i, "cell %d" % i, border=border, center=True)
        table.writeline()
        table.writecol(1, "in line 3, the second cell has a very long entry that will wrap many times to test this feature", border=border, ansicodes=["red", "bold"])
        table.writecol(2, "cell 2 also has some stuff but not quite as much", border=border)
        table.writecol(3, "but not cell 3")
        table.writecol(3, "but not cell 3", border=border, ansicodes=["magenta bg", "yellow"])
        table.newrow()
        table.writecol(0, "here is an extra long line with some super stuff going on - awesome!", border=border)
        table.writecol(1, "shorty", border=border)
        table.newrow()
        table.writecol(2, "just some junk", border=border)
        table.newrow()
        table.writecol(2, "centered", border=border, center=True)
        table.newrow()
        table.writecol(2, "centered2", border=border, ansicodes=["red", "underline"], center=True)
        table.newrow()
        table.writecol(2, "I want to be centered but I am too long", border=border)
        table.newrow()
        table.writecol(2, "I would normally wrap but I don't allow it", border=border, wrap=False)
        table.writecol(3, "Next to trunc", border=border)
        table.newrow()
        table.writecol(0, "Top pad", border=border, padding=(2,0,0,0))
        table.writecol(1, "Bottom pad", border=border, padding=(0,2,0,0))
        table.writecol(2, "Left padding", border=border, padding=(0,0,2,0))
        table.writecol(3, "Right pad", border=border, padding=(0,0,0,2))
        table.writecol(4, "All pad", border=border, padding=(2,2,2,2))
        table.newrow()
        table.writecol(0, "Top padding on a bigger cell", border=border, padding=(2,0,0,0))
        table.writecol(1, "Bottom padding on a bigger cell", border=border, padding=(0,2,0,0))
        table.writecol(2, "Left padding on a bigger cellding", border=border, padding=(0,0,2,0))
        table.writecol(3, "Right padding on a bigger cell", border=border, padding=(0,0,0,2))
        table.writecol(4, "All padding on a bigger cell", border=border, padding=(2,2,2,2))
        table.newrow()
        table.writecol(1, "Bottom left", border=border, ansicodes=["cyan", "underline"], padding=(0,2,2,0))
        table.writecol(4, "mid", border=border, center=True, padding=(2,2,2,2))
        table.newrow()
        table.writecol(0, ["Testing lists", "row 2"], border=border)
        table.writecol(1, ["centered", "list"], center=True, border=border)
        table.writecol(2, ["with", "", "some", "", "spaces", "", "and a long line at the end to finish it"], border=border)
        table.newrow()
            
if __name__ == '__main__':
    main()
