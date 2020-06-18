from struct import unpack

TOWN_TILESET = [
    "grass",
    "desert",
    "water",
    "chest",
    "block",
    "stairs_up",
    "brick",
    "stairs_down",
    "forest",
    "swamp",
    "harm",
    "door",
    "armory_sign",
    "inn_sign",
    "bridge",
    "desk"
]

DUNGEON_TILESET = [
    "block",
    "stairs_up",
    "brick",
    "stairs_down",
    "chest",
    "door",
    "princess",
    "unknown",
]

OVERWORLD_TILESET = [
    "grass",
    "desert",
    "hills",
    "mountains",
    "water",
    "block",
    "forest",
    "swamp",
    "town",
    "cave",
    "castle",
    "bridge",
    "stairs_down"
]

def town(rom, index):
    address = index * 5 + 0x24

    address, width, height, hmm = unpack("<HBBB", rom[address:address+5])
    address &= 0x7FFF
    width += 1
    height += 1

    print "%x" % hmm

    lines = []
    for i in range(height):
        line = []
        for i in range(0, width, 2):
            byte = ord(rom[address])

            if (index >= 10):
                byte &= 0x77

            line += [byte >> 4, byte & 0xF]

            address += 1

        lines += [line]

    return {
        'width': width,
        'height': height,
        'tiles': DUNGEON_TILESET if (index >= 13) else TOWN_TILESET,
        'map': lines
    }

def overworld(rom):
    lines = []

    for index, address in enumerate(unpack("<120H", rom[0x2653:0x2653+240])):
        address &= 0x7FFF

        line = []
        count = 120
        while count > 0:
            byte = ord(rom[address])
            t, c = byte >> 4, (byte & 0xF) + 1

            address += 1
            count -= c
            line += [t] * c
        
        lines += [line[:120]]

    return {
        'width': 120,
        'height': 120,
        'tiles': OVERWORLD_TILESET,
        'map': lines
    }
