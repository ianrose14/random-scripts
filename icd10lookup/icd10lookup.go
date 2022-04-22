package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"strings"
	"unicode"

	"golang.org/x/net/html"
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		s := strings.TrimSpace(scanner.Text())
		if s != "" {
			result, err := lookup(s)
			if err != nil {
				log.Printf("warning: failed to look up %q: %s", s, err)
			} else {
				fmt.Printf("%s\t%s\n", s, result)
			}
		}
	}

	if err := scanner.Err(); err != nil {
		log.Fatalf("failed to read from stdin: %s", err)
	}
}

func lookup(code string) (string, error) {
	urlstr := fmt.Sprintf("https://icdcodelookup.com/icd-10/codes/" + url.PathEscape(code))
	rsp, err := http.Get(urlstr)
	if err != nil {
		return "", err
	}
	defer func() { _ = drainAndClose(rsp.Body) }()

	if rsp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("bad response code: %s", rsp.Status)
	}

	root, err := html.Parse(rsp.Body)
	if err != nil {
		return "", err
	}

	n := findNode(root, "nuemd-icd-code-card")
	if n == nil {
		// yuck, just assume this is a "code not found" case, as opposed to a failure to parse a legit result
		return "CODE NOT FOUND", nil
	}

	var sb strings.Builder
	slurpText(n, &sb)

	s := sb.String()

	if s == "" {
		return "", fmt.Errorf("parse failure: found no text")
	}

	return s, nil
}

func findNode(n *html.Node, nodename string) *html.Node {
	if n.Type == html.ElementNode && n.Data == nodename {
		return n
	}
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		if result := findNode(c, nodename); result != nil {
			return result
		}
	}

	return nil
}

func hasClass(n *html.Node, classname string) bool {
	for _, elt := range n.Attr {
		if elt.Key == "class" && elt.Val == classname {
			return true
		}
	}
	return false
}

func slurpText(n *html.Node, dst *strings.Builder) {
	if n.Type == html.ElementNode && hasClass(n, "codeInfo") {
		for c := n.FirstChild; c != nil; c = c.NextSibling {
			if c.Type == html.TextNode {
				s := strings.TrimSpace(c.Data)
				s = strings.TrimLeftFunc(s, unicode.IsPunct)
				s = strings.TrimSpace(s)
				dst.WriteString(s)
			}
		}
		return
	}

	for c := n.FirstChild; c != nil; c = c.NextSibling {
		if c.Type == html.ElementNode {
			slurpText(c, dst)
		}
	}
}

// DrainAndClose discards any remaining bytes in r, then closes r.
// You have to read responses fully to properly free up connections.
// See https://groups.google.com/forum/#!topic/golang-nuts/pP3zyUlbT00
func drainAndClose(r io.ReadCloser) error {
	_, copyErr := io.Copy(ioutil.Discard, r)
	closeErr := r.Close()
	if closeErr != nil {
		return closeErr
	} else {
		return copyErr
	}
}
