# Teebr Makefile

VENV = venv

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


# Cleaning
# ------------------------

clean:
	rm -f *~
