# Teebr report Makefile

TARGET ?= rapport.pdf

SOURCES=$(wildcard *.tex) $(wildcard *.bib)

$(TARGET): $(SOURCES)
	./compile.sh

clean:
	$(RM) *~ *.out *.aux *.bbl *.blg *.toc *.log
