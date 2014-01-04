#!/usr/bin/env python2.7

#
# IMPORTS
#
from argparse import ArgumentParser
import httplib
import logging
from paste import httpserver
import signal
import socket
import ssl
import sys
import urllib2
import webapp2


#
# CONSTANTS
#
DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8080
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FORMAT = '[%(asctime)s] %(levelname)s %(name)s %(funcName)s -- %(message)s'


#
# GLOBALS
#
logger = logging.getLogger('wwwproxy')


#
# CLASSES
#

class ProxyRequestHandler(webapp2.RequestHandler):
  def head(self):
    url = self.request.GET.get('url')
    if not url:
      return webapp2.abort(httplib.BAD_REQUEST, 'Missing required GET parameter "url".')
    req = urllib2.Request(url)
    req.get_method = lambda: 'HEAD'
    self._request(req)

  def get(self):
    url = self.request.GET.get('url')
    if not url:
      return webapp2.abort(httplib.BAD_REQUEST, 'Missing required GET parameter "url".')

    req = urllib2.Request(url)
    self._request(req)

  def post(self):
    url = self.request.GET.get('url')
    if not url:
      return webapp2.abort(httplib.BAD_REQUEST, 'Missing required GET parameter "url".')

    req = urllib2.Request(url, data=self.request.body)
    self._request(req)

  def _request(self, req):
    try:
      rsp = urllib2.urlopen(req)
      self.response.status = rsp.code
      self.response.write(rsp.read())
      logger.info('successful fetch (%d response) from "%s"', rsp.code, req.get_full_url())
    except urllib2.HTTPError, e:
      self.response.status = e.code
      self.response.write(e.read())
      logger.info('HTTPError (%d response) from "%s"', e.code, req.get_full_url())
    except urllib2.URLError, e:
      self.response.status = httplib.INTERNAL_SERVER_ERROR
      self.response.write(str(e))
      logger.exception('failure fetching "%s"', req.get_full_url())


class RootHandler(webapp2.RequestHandler):
  def get(self):
    self.response.write('Hi...')


#
# FUNCTIONS
#

# monkey-patch for httplib to work around SSL issue
def monkeypatch_https_connect(self):
  """Connect to a host on a given (SSL) port."""
  sock = socket.create_connection((self.host, self.port),
                                  self.timeout, self.source_address)
  if self._tunnel_host:
    self.sock = sock
    self._tunnel()
  self.sock = ssl.wrap_socket(sock, self.key_file,
                              self.cert_file,
                              ssl_version=ssl.PROTOCOL_TLSv1)


#
# MAIN
#
def main():
  # override annoying python SIGINT handling
  signal.signal(signal.SIGINT, signal.SIG_DFL)

  parser = ArgumentParser('Simple web proxy')
  parser.add_argument('--host', default=DEFAULT_HOST, help='Address to bind to (default: %s)' % DEFAULT_HOST)
  parser.add_argument('-p', '--port', default=DEFAULT_PORT, help='Port to bind to (default: %s)' % DEFAULT_PORT)
  args = parser.parse_args()

  h = logging.StreamHandler(stream=sys.stdout)
  h.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT))
  h.setLevel(logging.DEBUG)  # enable everything; let the logger objects set the level threshold

  logger.handlers.append(h)
  logger.setLevel(logging.DEBUG)

  # reference: https://bugs.launchpad.net/ubuntu/+source/openssl/+bug/965371
  httplib.HTTPSConnection.connect = monkeypatch_https_connect

  routes = [('/', RootHandler), ('/proxy/', ProxyRequestHandler)]
  webapp = webapp2.WSGIApplication(routes=routes, debug=True)

  httpserver.serve(webapp, host=args.host, port=args.port, use_threadpool=True)


if __name__ == '__main__':
  main()
