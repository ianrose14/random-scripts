package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
)

func printAndEcho(w http.ResponseWriter, format string, args ...interface{}) {
	fmt.Printf(format+"\n", args...)
	fmt.Fprintf(w, format+"\n", args...)
}

func main() {
	port := flag.Int("port", 8000, "TCP port to listen on")
	flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Add("Content-Type", "text/plain")
		printAndEcho(w, "Method: %s", r.Method)
		printAndEcho(w, "URL: %s", r.Method)

		for k, v := range r.Header {
			printAndEcho(w, "headers[%q] = %v", k, v)
		}

		for k, v := range r.URL.Query() {
			printAndEcho(w, "querystring[%q] = %v", k, v)
		}

		r.ParseForm()

		for k, v := range r.PostForm {
			printAndEcho(w, "post[%q] = %v", k, v)
		}

		printAndEcho(w, "") // blank line to delimit requests
	})

	socket := fmt.Sprintf(":%d", *port)
	log.Printf("listening on %v", socket)
	http.ListenAndServe(socket, nil)
}
