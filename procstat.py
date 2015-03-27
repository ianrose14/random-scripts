#!/usr/bin/env python2.7

import sys

def echo(s):
  return s

states = {
  'R': 'Running',
  'S': 'Sleeping in an interruptible wait',
  'D': 'Waiting in uninterruptible disk sleep',
  'Z': 'Zombie',
  'T': 'Stopped (on a signal) or trace stopped',
  't': 'Tracing stop',
  'W': 'Paging',
  'X': 'Dead',
  'x': 'Dead',
  'K': 'Wakekill',
  'W': 'Waking',
  'P': 'Parked'
  }

def expand_state(s):
  return

def ticks_to_millis(s):
  return '%d millis' % (int(s) * 10)

keys = [
  ('pid', echo),
  ('filename', lambda s: s[1:-1]),  # strip enclosing parens
  ('state', expand_state),
  ('ppid', echo),
  ('pgrp', echo),
  ('session', echo),
  ('tty_nr', echo),
  ('tpgid', echo),
  ('flags', echo),
  ('minflt (minor faults; no page load)', echo),
  ('cminflt (children minor faults; no page load)', echo),
  ('majflt (major faults; yes page load)', echo),
  ('cmajflt (children major faults; yes page load)', echo),
  ('utime (user mode)', ticks_to_millis),
  ('stime (system mode)', ticks_to_millis),
  ('cutime (children user mode)', ticks_to_millis),
  ('cstime (children system mode)', ticks_to_millis),
  ('priority', echo),
  ('nice', echo),
  ('num_threads', echo),
  ('itrealvalue (SIGALRM interval)', echo),
  ('starttime (since boot)', ticks_to_millis),
  ('vsize (virt. mem bytes)', echo),
  ('rss (res. pages)', echo),
  ('rsslim (rss bytes soft limit)', echo),
  ('startcode', echo),
  ('endcode', echo),
  ('startstack', echo),
  ('kstkesp', echo),
  ('kstkeip', echo),
  ('signal', echo),
  ('blocked', echo),
  ('sigignore', echo),
  ('sigcatch', echo),
  ('wchan', echo),
  ('nswap', echo),
  ('cnswap', echo),
  ('exit_signal', echo),
  ('processor', echo),
  ('rt_priority', echo),
  ('policy', echo),
  ('delayacct_blkio_ticks', echo),
  ('guest_time', ticks_to_millis)
]


def main():
  while True:
    line = sys.stdin.readline()
    if len(line) == 0:
      break  # EOF

    parts = line.strip().split()

    for i in range(len(parts)):
      if i >= len(keys):
        break
      label, f = keys[i]
      print '%s: %s' % (label, f(parts[i]))


if __name__ == '__main__':
  main()
