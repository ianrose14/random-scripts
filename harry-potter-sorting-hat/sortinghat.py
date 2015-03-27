#!/usr/bin/env python2.7

import curses
import random
import subprocess
import time


# globals
houses = [None, 'hufflepuff.mp3', 'ravenclaw.mp3', 'slytherin.mp3']


def next_file():
  queue = []

  while True:
    if len(queue) == 0:
      indexes = range(len(houses))
      random.shuffle(indexes)
      for index in indexes:
        if index == 0:
          # special case for gryffindor because we have 2 options; pick one randomly
          filename = random.choice(['gryffindor1.mp3', 'gryffindor2.mp3'])
        else:
          filename = houses[index]
        queue.append(filename)

    print 'next up:', queue[0]
    yield queue.pop(0)


def play_mp3(filename):
  subprocess.call(['afplay', filename])


def run(stdscr):
  stdscr.keypad(True)
  curses.cbreak()

  # first 2 are hard-coded
  stdscr.getch()
  play_mp3('hufflepuff.mp3')

  stdscr.getch()
  play_mp3('slytherin.mp3')

  for filename in next_file():
    stdscr.getch()
    play_mp3(filename)


#
# MAIN
#
def main():
  random.seed(time.time())
  curses.wrapper(run)


if __name__ == '__main__':
  main()
