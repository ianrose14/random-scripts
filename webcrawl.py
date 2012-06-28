#!/usr/bin/env python

import formatter
import htmllib
import httplib
from optparse import OptionParser
import re
import urlparse

class Crawler:
    def __init__(self, parser, handler, verbose=0):
        self.parser = parser
        self.handler = handler
        self.verbose = verbose

    def crawl(self, url, samehost=False, depth=None, limit=None):
        self.crawled = set()
        self.targets = [(url, 0)]

        if samehost:
            (scheme, netloc, path, url_params, query, fragment) = urlparse.urlparse(url)
            basehost = netloc
        else:
            basehost = None

        c = 0
        while 1:
            if len(self.targets) == 0:
                break

            if limit is not None and c >= limit:
                break

            (target, d) = self.targets[0]
            self.targets.pop(0)

            if self.verbose >= 2:
                print "crawling %s" % url

            if not self._crawl_page(target, basehost):
                continue

            c += 1

            if len(self.handler.matches) > 0:
                print url
                # don't print more than 5 matches (gets a bit verbose)
                for match in self.handler.matches[:5]:
                    print " "*4, match
                self.handler.clear()

            if depth is not None:
                if d >= depth:
                    continue

            # ok to delve further
            for link in self.parser.anchorlist:
                print link
                abslink = urlparse.urljoin(url, link)
                if verbose >= 2:
                    print "added link to %s" % url
                if abslink not in self.crawled:
                    self.targets.append((abslink, depth+1))

    def _crawl_page(self, url, basehost):
        (scheme, netloc, path, url_params, query, fragment) = urlparse.urlparse(url)
        if query != "":
            resource = path + "?" + query
        else:
            resource = path

        if basehost is not None and netloc != basehost:
            if self.verbose >= 2:
                print "...skipping %s (host different)" % url
            return False
        
        if scheme == "file":
            conn = FileConnection()
        elif scheme == "http":
            conn = httplib.HTTPConnection(netloc, strict=True)
        elif scheme == "https":
            conn = httplib.HTTPSConnection(netloc, strict=True)
        else:
            raise ValueError("bad url scheme: %s" % scheme)

        conn.request("GET", resource, body=None, headers={})
        self.crawled.add(url)
        try:
            response = conn.getresponse()
        except StandardError, e:
            print url, repr(e)
            return False

        if response.status >= 300 and response.status < 400:
            loc = response.getheader("location", None)
            if loc is None:
                if self.verbose >= 1:
                    print "%03d %s from %s" % (response.status, response.reason, url)
            else:
                if self.verbose >= 2:
                    print "...following redirection from %s to %s" % (url, loc)
                return self._crawl_page(loc)

        elif response.status == 200:
            if self.verbose >= 2:
                print "%03d %s from %s" % (response.status, response.reason, url)

            while 1:
                s = response.read(4096)
                if s == "":
                    break
                self.parser.feed(s)
        else:
            if self.verbose >= 1:
                print "%03d %s from %s" % (response.status, response.reason, url)

class FileConnection:
    def __init__(self):
        self.fi = None

    def request(self, method, resource, body=None, headers={}):
        if self.fi is not None:
            self.fi.close()
        self.fi = open(resource, "r")

    def getresponse(self):
        r = FileResponse(self.fi)
        self.fi = None
        return r

class FileResponse:
    def __init__(self, fi):
        self.status = 200
        self.reason = "Okay"
        self.fi = fi

    def getheader(self, header, default=None):
        return default

    def read(self, len=None):
        return self.fi.read(len)
            
class LinkParser(htmllib.HTMLParser):
    def __init__(self, writer):
        htmllib.HTMLParser.__init__(self, formatter.AbstractFormatter(writer))
        self.anchorlist = []

    def anchor_bgn(self, href, name, type):
        self.anchorlist.append(href)

class TextHandler(formatter.NullWriter):
    def __init__(self, pattern):
        formatter.NullWriter.__init__(self)
        self.pattern = pattern
        self.matches = []

    def _handle_text(self, data):
        matches = self.pattern.findall(data)
        for match in matches:
            self.matches.append(match)

    def clear(self):
        self.matches = []

    def send_flowing_data(self, data):
        self._handle_text(data)

    def send_literal_data(self, data):
        self._handle_text(data)

    def send_label_data(self, data):
        self._handle_text(data)

def main():
    parser = OptionParser("%prog [options] URL PATTERN")
    parser.add_option("-d", "--depth", type="int", default=None)
    parser.add_option("-n", "--num", type="int", default=None)
    parser.add_option("-v", "--verbose", type="int", default=0)
    parser.add_option("--same-host", action="store_true", default=False)
    (opts, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("exactly 2 arguments required")

    (url, regex) = args

    pat = re.compile(regex, flags=re.IGNORECASE)
    handler = TextHandler(pat)
    parser = LinkParser(handler)
    crawler = Crawler(parser, handler, verbose=opts.verbose)
    crawler.crawl(url, samehost=opts.same_host, depth=opts.depth, limit=opts.num)

if __name__ == '__main__':
    main()

