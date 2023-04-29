.PHONY: compile clean stop

SHELL:=/usr/bin/bash
HANGAR:=/home/vagrant/Hangar/
BLD=build
BLD_BMV2=$(BLD)/BMv2

compile:
	make -C $(HANGAR) -f $(HANGAR)/Makefile $(TARGET_FILES)

clean:
	make -C $(HANGAR) -f $(HANGAR)/Makefile clean

stop:
	@mn -c
