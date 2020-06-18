GAME_CODE=DQPM
GAME_TITLE=DragonQuest
TARGET=test.min

SOURCES = $(shell find src -name "*.s") $(shell find src -name "*.c")

include toolchain/pokemini.mk

CFLAGS += -Isrc/include
