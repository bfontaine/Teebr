# Teebr Makefile

VENV = ./venv
SRC  = teebr
PWD  = $(shell pwd)

.PHONY: clean compile-assets deploy deps run collect

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

#freeze: $(VENV)
#	$(PIP) freeze >| $(REQS)

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

# DB
# ------------------------

# peewee removes the leading slash of the path, hence the three slashes here
# https://github.com/coleifer/peewee/issues/557
DB = "sqlite:///$(PWD)/db/teebr.db"
MIGRATIONS_DIR = db/migrations
MIGRATE_FLAGS = --directory $(MIGRATIONS_DIR) --database $(DB)
MIGRATE = $(BIN)pw_migrate

$(MIGRATIONS_DIR):
	mkdir -p $@
	touch $@/conf.py

create-migration: $(MIGRATIONS_DIR)
	[ "x$(MIGRATION_NAME)" != "x" ] && \
		$(MIGRATE) create $(MIGRATE_FLAGS) "$(MIGRATION_NAME)" || \
		( echo 'Set $$(MIGRATION_NAME) to run this.'; false )

run-migrations: $(MIGRATIONS_DIR)
	$(MIGRATE) migrate $(MIGRATE_FLAGS) -v


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

seed-db:
	$(BIN)python collect_stream.py

collect:
	$(BIN)python collect_timelines.py

# Deploy
# ------------------------

deploy:
	./deploy.sh

# Cleaning
# ------------------------

clean:
	$(RM) *~ *.log *.log.1
