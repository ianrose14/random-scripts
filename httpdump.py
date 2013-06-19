#!/usr/bin/env python2.7

#
# IMPORTS
#
from argparse import ArgumentParser
from paste import httpserver
import signal
import webapp2


#
# CLASSES
#
class DumpHandler(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('method: %s\n' % self.request.method)
    self.response.write('url: %s\n' % self.request.url)
    for k, v in self.request.headers.iteritems():
      self.response.write('headers[\'%s\']: %s\n' % (k, v))
    if len(self.request.GET) > 0:
      for k, v in self.request.GET.iteritems():
        self.response.write('GET[\'%s\']: %s\n' % (k, v))
    if len(self.request.POST) > 0:
      for k, v in self.request.POST.iteritems():
        self.response.write('POST[\'%s\']: %s\n' % (k, v))


#
# MAIN
#

def main():
  # override annoying python SIGINT handling
  signal.signal(signal.SIGINT, signal.SIG_DFL)

  parser = ArgumentParser(description='A webserver')
  parser.add_argument('-p', '--port', default=8080, type=int, help='Server port')
  args = parser.parse_args()

  routes = [(r'/.*', DumpHandler)]
  webapp = webapp2.WSGIApplication(routes=routes, debug=True)
  httpserver.serve(webapp, port=args.port, use_threadpool=True, daemon_threads=True)


if __name__ == '__main__':
  main()
