ifeq ($(OS), Windows_NT)
	WINE :=
	TOOLCHAIN := $(dir $(lastword $(MAKEFILE_LIST)))
else # In Unix we use wine and assume the tools are in the PATH
	WINE := wine
	TOOLCHAIN := z:$(abspath $(dir $(lastword $(MAKEFILE_LIST))))
endif

OBJECTS = $(patsubst %.c,%.obj,$(patsubst %.s,%.obj,$(SOURCES)))

LKFLAGS = -v -Ml -Tlc-d$(TOOLCHAIN)/ETC/pokemini.dsc -Tlk-L$(TOOLCHAIN)/LIB
CFLAGS 	= -O2 -Ml -I$(TOOLCHAIN)/INCLUDE -Ta-O -Tc-v 
ASFLAGS = -O -Ml

CC88 = $(WINE) $(TOOLCHAIN)/BIN/CC88.EXE
AS88 = $(WINE) $(TOOLCHAIN)/BIN/AS88.EXE

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC88) $(LKFLAGS)  -o $@ $^

%.obj: %.c
	echo $(MAKEFILES)
	$(CC88) $(CFLAGS) -c -o $@ $<

%.obj: %.s
	$(AS88) $(ASFLAGS) -o $@ $<

clean:
	rm -Rf $(TARGET) $(OBJECTS)

.phony: all clean
