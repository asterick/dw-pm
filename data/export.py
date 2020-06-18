import maps
from types import TupleType

REMAP = {
    'water': '1',
    'grass': '2',
    'forest': '3',
    'hills': '4',
    'mountains': '5',   
    'desert': '6',
    'swamp': '7',
    'brick': '8',
    'block': '9',
    'harm': '10',
    'desk': '11',

    'door': ('13', '8'),
    'stairs_down': ('14', '24'),
    'stairs_up': ('15', '8'),
    'bridge': ('16', '1'),
    'chest': ('17', '8'),

    'cave': ('18', -1),
    'castle': ('19', -1),
    'town': ('20', -1),
    'armory_sign': ('21', '2'),
    'inn_sign': ('22', '2'),
    'princess': ('23', '8'),
}

def export(n, m, overworld = True):
    width, height = m['width'], m['height']

    t = []
    objs = []

    for y, line in enumerate(m['map']):
        for x, i in enumerate(line):
            k = REMAP[m['tiles'][i]]
            
            if type(k) == TupleType:
                o, r = k
                objs += ['<object id="1" name="%s" gid="%s" x="%i" y="%i" width="16" height="16"/>' % (m['tiles'][i], o, x * 16, (y+1) * 16)]
                
                if type(r) == type(1):
                    if len(t) + r >= 0:
                        r = t[r]
                    else:
                        r = '12'

                print r
                t += [r]
            else:
                t += [k]
                p = k

    with file(n, "w") as fo:
        fo.write("""<?xml version="1.0" encoding="UTF-8"?>
        <map version="1.2" tiledversion="1.3.5" orientation="orthogonal" renderorder="right-down" width="%i" height="%i" tilewidth="16" tileheight="16" infinite="0" nextlayerid="2" nextobjectid="1">
        <tileset firstgid="1" name="tileset" tilewidth="16" tileheight="16" tilecount="36" columns="12">
        <image source="10199.png" width="192" height="48"/>
        </tileset>
        <layer id="1" name="Tile Layer 1" width="%i" height="%i">
        <data encoding="csv">
        %s
        </data>
        </layer>
        <objectgroup id="3" name="Object Layer 1">
        %s
        </objectgroup>
        </map>""" % (width, height, width, height,','.join(t), ''.join(objs)))

with file("Dragon Warrior (USA) (Rev A).nes", "rb") as rom:
    rom = rom.read()[0x10:]

for i in range(28):
    export("maps/%i.tmx" % i, maps.town(rom, i))


export('maps/overworld.tmx', maps.overworld(rom))