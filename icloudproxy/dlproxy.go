package main

import (
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
)

var (
	targets = make(chan string, 10000)
)

func downloadOne(u string, i int) {
	rsp, err := http.Get(u)
	if err != nil {
		log.Printf("failed to fetch (%s): %s", err, u)
		return
	}

	defer rsp.Body.Close()

	if rsp.StatusCode > 299 {
		log.Printf("failed to fetch (http %s): %s", rsp.Status, u)
		return
	}

	suffix := ".wut"
	switch rsp.Header.Get("Content-Type") {
	case "image/jpeg":
		suffix = "jpg"
	case "image/png":
		suffix = "png"
	case "image/gif":
		suffix = "gif"
	case "image/tiff":
		suffix = "tiff"
	}

	filename := fmt.Sprintf("imgs/img%d.%s", i, suffix)
	fp, err := os.Create(filename)
	if err != nil {
		log.Printf("failed to create %s: %s", filename, err)
		return
	}

	defer fp.Close()

	if _, err := io.Copy(fp, rsp.Body); err != nil {
		log.Printf("failed to copy body to file: %s", err)
		return
	}
}

func downloader() {
	i := 0

	for u := range targets {
		downloadOne(u, i)
		i += 1
	}
}

func handler(w http.ResponseWriter, r *http.Request) {
	w.Header().Add("Access-Control-Allow-Origin", "*")

	u := r.URL.Query().Get("q")
	targets <- u

	fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
}

func main() {
	go downloader()

	http.HandleFunc("/", handler)
	http.ListenAndServe(":9933", nil)
}
