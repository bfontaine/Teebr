# Teebr Makefile

report/%:
	cd $(dir $@) && $(MAKE) $(notdir $@)
