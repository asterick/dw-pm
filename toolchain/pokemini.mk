ifeq ($(OS), Windows_NT)
	WINE :=
else # In Unix we use wine and assume the tools are in the PATH
	WINE := wine
endif

TOOLCHAIN := $(dir $(lastword $(MAKEFILE_LIST)))
OBJECTS = $(patsubst %.c,%.obj,$(patsubst %.s,%.obj,$(SOURCES)))

LKFLAGS = -v -Ml -Tlk-d$(TOOLCHAIN)ETC/pokemini.dsc -Tlc-d$(TOOLCHAIN)ETC/pokemini.dsc -Tlk-L$(TOOLCHAIN)LIB
CFLAGS 	= -O2 -Ml -I$(TOOLCHAIN)INCLUDE -Ta-O -Tc-v
ASFLAGS = -O -Ml

CC88 = $(WINE) $(TOOLCHAIN)BIN/CC88.EXE
AS88 = $(WINE) $(TOOLCHAIN)BIN/AS88.EXE

all: $(TARGET) $(TARGET).obj
	python3 $(TOOLCHAIN)dump.py $(TARGET).obj

$(TARGET): $(TARGET).hex
	python3 $(TOOLCHAIN)extract.py $(TARGET).map $@ $<

$(TARGET).hex: $(OBJECTS)
	$(CC88) $(LKFLAGS) -Tlc-f3 -o $@ $^

$(TARGET).obj: $(OBJECTS)
	$(CC88) $(LKFLAGS) -o $@ $^

%.obj: %.c
	echo $(MAKEFILES)
	$(CC88) $(CFLAGS) -c -o $@ $<

%.obj: %.s
	$(AS88) $(ASFLAGS) -o $@ $<

clean:
	rm -f $(TARGET) $(TARGET).hex $(OBJECTS)

.phony: all clean
