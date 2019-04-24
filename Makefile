TARGET=test.min

SOURCES = src/main.c src/startup.s src/isr.c

include toolchain/pokemini.mk

CFLAGS += -Isrc/include
