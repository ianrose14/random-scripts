.PHONY: all

all: tstodate datetots run

%: %.go
	go build -o $@ $<
