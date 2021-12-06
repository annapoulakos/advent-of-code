SHELL := /bin/zsh
.SHELLFLAGS := -ue -o pipefail -c
.ONESHELL:
.DELETE_ON_ERROR:
.SUFFIXES:
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules


commands/d%.py:
	cp templates/default.py.tpl $(@)
	sed -i '' 's/{VALUE}/$(*)/' $(@)
	touch data/day-$(*).txt
	touch data/day-ex-$(*).txt
