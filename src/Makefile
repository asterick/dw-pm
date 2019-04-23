WINE = wine
C88_TOOLCHAIN_DIR = ../bin
C88 = $(WINE) $(C88_TOOLCHAIN_DIR)/c88
ALC88 = $(WINE) $(C88_TOOLCHAIN_DIR)/alc88

TARGET=test

SOURCES = main.c
OBJECTS = $(SOURCES:.c=.obj)

CFLAGS = -O2 -Ml -Iinclude

all: $(TARGET).out

clean:
	rm -Rf $(OBJECTS) $(TARGET).out

$(TARGET).out: $(OBJECTS)
	echo $(C88) -Ml -cl -o $@ $^

%.obj: %.c
	$(C88) $(CFLAGS) -o $@ $<

.phony: all clean
