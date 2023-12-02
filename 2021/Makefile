SHELL := /bin/zsh
.SHELLFLAGS := -ue -o pipefail -c
.ONESHELL:
.DELETE_ON_ERROR:
.SUFFIXES:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

run-%:
	@aoc d$(*) -t 1
	@aoc d$(*) 1
	@aoc d$(*) -t 2
	@aoc d$(*) 2


commands/d%.py:
	cp templates/default.py.tpl $(@)
	sed -i '' 's/{VALUE}/$(*)/' $(@)
	touch data/day-$(*).txt
	touch data/day-ex-$(*).txt
