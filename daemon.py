#!/usr/bin/env python

"""Disk And Execution MONitor (Daemon)

Adapted heavily from
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/278731
(original author: Chad J. Schroeder)

and

http://www.noah.org/wiki/Daemonize_Python
"""

import atexit
import errno
import os
import sys
import types

class InvalidPidfileError(StandardError):
    pass

class ProcessExistsError(StandardError):
    pass

def check_process(pid):
    try:
        os.kill(pid, 0)
    except OSError, e:
        if e[0] == errno.ESRCH:
            # no such process (not running)
            return False
        else:
            # some other error in os.kill()
            raise
    else:
        # is os.kill() does not raise an error, that means the process is running
        return True

# a note on exit() or _exit():
# _exit is like exit(), but it doesn't call any functions registered
# with atexit (and on_exit) or any registered signal handlers.  It also
# closes any open file descriptors.  Using exit() may cause all stdio
# streams to be flushed twice and any temporary files may be unexpectedly
# removed.  It's therefore recommended that child branches of a fork()
# and the parent branch(es) of a daemon use _exit().

def daemonize(pidfile=None, stdin='/dev/null', stdout='/dev/null',
              stderr='/dev/null'):
   """Detach a process from the controlling terminal and run it in the
   background as a daemon.
   """

   if pidfile:
      # open pidfile before daemonizing
      pidfileobj = openpidfile(pidfile, ex_exist=False)

   pid = os.fork()

   if pid > 0:  # parent
      os._exit(0)

   # (else, child)

   # To become the session leader of this new session and the process group
   # leader of the new process group, we call os.setsid().  The process is
   # also guaranteed not to have a controlling terminal.
   os.setsid()

   pid = os.fork()	# Fork a second child.
   
   if pid > 0:  # parent
      if pidfile:
         # write new pid to pidfile
         print >>pidfileobj, "%d" % pid
         pidfileobj.close()
      os._exit(0)

   # (else, child)

   # register exit handler to delete the pidfile when we are done (must do this
   # before chdir-ing away from the current directory)
   if pidfile:
      abspid = os.path.abspath(pidfile)
      atexit.register(lambda: os.unlink(abspid))

   os.chdir("/")

   # Just redirect stdin, stdout, and stderr.  Some implementations like to close
   # all open file descriptors, but the functionality implemented here copies
   # that of daemon(3) and daemon(8) on FreeBSD 6.2-STABLE.
   if type(stdin) == types.FileType:
      si = stdin
   else:
      si = open(stdin, 'r')
   
   if type(stdout) == types.FileType:
      so = stdout
   else:
      so = open(stdout, 'a+')
   
   if type(stderr) == types.FileType:
      se = stderr
   else:
      se = open(stderr, 'a+', 0)  # unbuffered
   
   os.dup2(si.fileno(), sys.stdin.fileno())
   os.dup2(so.fileno(), sys.stdout.fileno())
   os.dup2(se.fileno(), sys.stderr.fileno())

def openpidfile(filename, ex_exist=True):
    dirname = os.path.dirname(filename)
    if len(dirname) > 0:
        try:
            os.makedirs(dirname)
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
    
    # need to use os.open() instead of builtin open() for special flags
    try:
        fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0664);
    except OSError, e:
        if (not ex_exist) and e[0] == errno.EEXIST:
            # ok, pidfile already exists, but is process running?
            fi = open(filename, 'r')
            pidtxt = fi.read().strip()
            fi.close()
            
            # if pidfile is empty, assume this means that process isn't running
            if pidtxt != '':
                try:
                    pid = int(pidtxt)
                except ValueError:
                    raise InvalidPidfileError("invalid content: '%s'" % pidtxt)

                if check_process(pid):
                    # process is running
                    raise ProcessExistsError(pid)

            # if we get to here, then we don't think the process is running -
            # delete the pidfile then re-open it as though it never existed
            # (note: intentionally no exception trapping for this second opening)
            os.unlink(filename)
            fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0664);
        else:
            # some other error in os.open(), or caller wants to receive an
            # exception if pidfile exists
            raise
    return os.fdopen(fd, 'w')

if __name__ == "__main__":
   """A simple test of daemonize()"""

   pidfile = "daemonize-test.pid"
   print "pid=%d, pgid=%d" % (os.getpid(), os.getpgid(os.getpid())) + \
         ", ppid=%d | starting deamonize() test..." % os.getppid() + \
         " pidfile=\"%s\"" % pidfile
   
   daemonize(pidfile=pidfile, stdout=sys.stdout)

   print "pid=%d, pgid=%d" % (os.getpid(), os.getpgid(os.getpid())) + \
         ", ppid=%d | done with deamonize()... sleeping for 10s" % os.getppid()
   
   import time
   time.sleep(10)

   print "pid=%d, pgid=%d" % (os.getpid(), os.getpgid(os.getpid())) + \
         ", ppid=%d | done sleeping.  exitting." % os.getppid()

   sys.exit(0)
