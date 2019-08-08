# Use wine if installed
WINE := ${shell which wine}
TOOLCHAIN := $(dir $(lastword $(MAKEFILE_LIST)))
OBJECTS = $(patsubst %.c,%.obj,$(patsubst %.s,%.obj,$(SOURCES)))

LKFLAGS = -v -Ml -Tlk-d$(TOOLCHAIN)ETC/pokemini.dsc -Tlc-d$(TOOLCHAIN)ETC/pokemini.dsc -Tlk-L$(TOOLCHAIN)LIB
CFLAGS 	= -O2 -Ml -I$(TOOLCHAIN)INCLUDE -Ta-O
ASFLAGS = -O -Ml

CC88 = $(WINE) $(TOOLCHAIN)BIN/CC88.EXE
AS88 = $(WINE) $(TOOLCHAIN)BIN/AS88.EXE
EXPORT_FLAGS=

ifdef GAME_CODE
EXPORT_FLAGS += --code=$(GAME_CODE)
endif

ifdef GAME_TITLE
EXPORT_FLAGS += --title=$(GAME_TITLE)
endif

all: $(TARGET)

$(TARGET): $(TARGET).obj
	python3 $(TOOLCHAIN)extract.py $(EXPORT_FLAGS) --output $@ $<

$(TARGET).obj: $(OBJECTS)
	$(CC88) $(LKFLAGS) -o $@ $^

%.obj: %.c
	echo $(MAKEFILES)
	$(CC88) $(CFLAGS) -c -o $@ $<

%.obj: %.s
	$(AS88) $(ASFLAGS) -o $@ $<

clean:
	rm -f $(TARGET) $(TARGET).obj $(TARGET).map $(OBJECTS)

.phony: all clean
