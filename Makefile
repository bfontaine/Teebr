# Teebr Makefile

VENV = venv
SRC  = teebr

.PHONY: clean deps

# Docs
# ------------------------

report/%:
	cd $(dir $@) && $(MAKE) $(notdir $@)


# Dependencies
# ------------------------

BIN  ?= $(VENV)/bin/
PIP   = $(BIN)pip

REQS  = requirements.txt

deps: $(VENV) requirements.txt
	$(PIP) install -r $(REQS)

freeze: $(VENV)
	$(PIP) freeze >| $(REQS)

$(VENV):
	virtualenv $@


# Assets
# ------------------------

LESSC = lessc

STATIC    = static
CSS_ROOT  = $(STATIC)/css
JS_ROOT   = $(STATIC)/js

CSS_TARGET = $(CSS_ROOT)/app.css

LESS_BASE = $(CSS_ROOT)/app.less
LESS_SOURCES = $(wildcard static/css/*.less)

compile-assets: $(CSS_TARGET)

$(CSS_TARGET): $(LESS_SOURCES)
	$(LESSC) $(LESS_BASE) > $@


# I18N
# ------------------------

PYBABEL=$(BIN)pybabel
I18N_DIR=translations

babel-extract:
	$(PYBABEL) extract -F babel.cfg -k lazy_gettext -o messages.pot .
	$(PYBABEL) update -i messages.pot -d $(I18N_DIR)

babel-compile:
	$(PYBABEL) compile -d $(I18N_DIR)


# Run
# ------------------------

run:
	$(BIN)gunicorn app:app


# Cleaning
# ------------------------

clean:
	rm -f *~
