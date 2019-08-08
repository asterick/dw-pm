TARGET=test.min

SOURCES = $(shell find src -name "*.c") $(shell find src -name "*.s")

include toolchain/pokemini.mk

CFLAGS += -Isrc/include
