.PHONY: all clean

P4C:=p4c-bm2-ss

BLD=build
BLD_BMV2=$(BLD)/BMv2

TARGET=TARGET_BMV2

all: $(BLD_BMV2)/networks/ALV/ALV.json

clean:
	rm -fr $(BLD)

$(BLD_BMV2)/%.json: %.p4
	mkdir -p `dirname $@`
	$(P4C) --emit-externs -I lib $< -o $@ --target bmv2 --arch v1model -DTARGET_BMV2
