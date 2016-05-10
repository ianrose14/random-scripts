package main

import (
	"fmt"
	"math/rand"
	"os"
	"os/exec"
	"time"
)

var voices = []string{
	"Daniel",
	"Karen",
	"Moira",
	"Tessa",
}

func main() {
	i := rand.New(rand.NewSource(time.Now().UnixNano())).Intn(len(voices))
	voice := voices[i]

	args := os.Args[1:]
	if len(args) == 0 {
		fmt.Fprintf(os.Stderr, "usage: run COMMAND [ARGS...]\n")
		os.Exit(2)
	}

	proc := exec.Command("time", args...)
	proc.Stderr = os.Stderr
	proc.Stdin = os.Stdin
	proc.Stdout = os.Stdout

	if err := proc.Run(); err != nil {
		exec.Command("say", "-v", voice, "Command complete.  Failed.").Run()
	} else {
		exec.Command("say", "-v", voice, "Command complete.  Success.").Run()
	}
}
