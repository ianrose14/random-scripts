#!/usr/bin/env python2.7

"""
Run a task repeatedly at a fixed interval.
"""

#
# IMPORTS
#
import time
import threading


#
# CLASSES
#
class RepeatingTimer:
  def __init__(self, interval, target, thread=None, name=None):
    if not thread:
      thread = threading.Thread(target=self._run, name=name, args=(interval, target))

    self.thread = thread
    self.cancelled = False  # thread-safe by rule of the interpreter (see http://effbot.org/zone/thread-synchronization.htm)

  def _run(self, interval, target):
    next = time.time() + interval
    while True:
      self._sleep_until(next)
      if self.cancelled:
        break
      # else, call the target function and the re-loop for the next interval
      target()
      next += interval

  def _sleep_until(self, t):
    left = t - time.time()
    while left > 0:
      time.sleep(left)
      left = t - time.time()

  def cancel(self):
    self.cancelled = True

  def start(self):
    # bombs if thread has already been started
    self.thread.start()


#
# MAIN
#
def main():
  """ Super-dumb test. """
  # override annoying python SIGINT handling
  import signal
  signal.signal(signal.SIGINT, signal.SIG_DFL)

  def printit():
    print time.time(), 'tick!'

  timer = RepeatingTimer(5, printit)
  print time.time(), 'starting'
  timer.start()
  time.sleep(22)
  print time.time(), 'cancelling'
  timer.cancel()
  print time.time(), 'joining'
  timer.thread.join()
  print time.time(), 'and.... done!'


if __name__ == "__main__":
  main()
