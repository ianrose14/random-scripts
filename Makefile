.PHONY: all run

all: run

%: %.go
	go build -o $@ $<
