#! /bin/bash

__compile_tex() {
    local file=$1
    local extended=$2
    local tex=${file}.tex

    sleep 0.2
    pdflatex $tex

    if [ ! -z "$extended" ]; then
        bibtex $file
        bibtex $file
        pdflatex $tex
    fi

    pdflatex $tex
}

__compile_tex rapport 1
