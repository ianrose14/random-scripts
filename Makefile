.PHONY: all run

all: run

run: run.go
	go build -o run run.go
