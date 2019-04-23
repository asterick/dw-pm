WINE = wine
C88_TOOLCHAIN_DIR = ~/.wine/drive_c/EPSON/S1C88/BIN

CC88 = $(WINE) $(C88_TOOLCHAIN_DIR)/CC88.EXE
AS88 = $(WINE) $(C88_TOOLCHAIN_DIR)/AS88.EXE

TARGET=test.min

SOURCES = main.c startup.s isr.c
OBJECTS = $(patsubst %.c,%.obj,$(patsubst %.s,%.obj,$(SOURCES)))

LKFLAGS = -v -Ml -Tlc-d..\\etc\\pokemini.dsc
CFLAGS 	= -O2 -Ml -Iinclude -Ta-O -Tc-v
ASFLAGS = -O -Ml

all: $(TARGET)

clean:
	rm -Rf $(OBJECTS) $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC88) $(LKFLAGS)  -o $@ $^

%.obj: %.c
	$(CC88) $(CFLAGS) -c -o $@ $<

%.obj: %.s
	$(AS88) $(ASFLAGS) -o $@ $<

.phony: all clean
