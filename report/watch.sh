#! /bin/bash
fswatch  *.tex *.bib | xargs -n1 ./compile.sh
