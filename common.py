#!/usr/bin/env python2.7

#
# IMPORTS
#
import logging
import sys
import time


#
# CONSTANTS
#

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = '[%(asctime)s] %(levelname)s %(name)s %(funcName)s -- %(message)s'


#
# GLOBALS
#
__all__ = ['asciify', 'configure_logging', 'dt_to_ts', 'extract_attrs']


#
# METHODS
#

def asciify(s):
  return ''.join([x if ord(x) < 128 else '?' for x in s])


def configure_logging(loggers, outfile, debug):
  if outfile is None:
    h = logging.StreamHandler(stream=sys.stdout)
  else:
    h = logging.handlers.WatchedFileHandler(outfile)

  h.setLevel(logging.DEBUG)  # enable everything; let the logger objects set the level threshold
  h.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT))

  for l in loggers:
    l.handlers.append(h)

    if debug:
      l.setLevel(logging.DEBUG)
    else:
      l.setLevel(logging.INFO)


def dt_to_ts(dt):
  return time.mktime(dt.timetuple())


def extract_attrs(obj, attrs, handlers):
  """ Return a dict-view of an object, using only a whitelist of attributes. """
  d = {}
  for attr in attrs:
    v = getattr(obj, attr)
    f = handlers.get(attr)
    if f:
      v = f(v)
    d[attr] = v
  return d
