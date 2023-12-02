SHELL := /bin/zsh
.SHELLFLAGS := -ue -o pipefail -c
.ONESHELL:
#.DELETE_ON_ERROR:
.SUFFIXES:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

YEAR = 2021
AOC_URL_PUZZLE := https://adventofcode.com/$(YEAR)/day

data/day-ex-%.txt:
	python utils/fetch.py $(YEAR) $(day) > $(@)

data/day-%.txt: data/day-ex-%.txt
	curl -H "Cookie: session=$(AOC_SESSION_COOKIE)" $(AOC_URL_PUZZLE)/$(*)/input -o $(@)

fetch: data/day-$(day).txt data/day-ex-$(day).txt



build:


clean:
	rm data/day-$(day).txt
	rm data/day-ex-$(day).txt
.PHONY: clean
