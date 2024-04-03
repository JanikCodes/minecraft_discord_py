from Classes import Block
from session import session

air = Block(1, name="Air", solid=0, gravity=0, light_level=10, z=0, debug_color="#0096FF")
session.merge(air)

grass = Block(2, name="Grass", solid=1, gravity=0, light_level=0, z=1, debug_color="#32B32B")
session.merge(grass)

stone = Block(3, name="Stone", solid=1, gravity=0, light_level=0, z=1, debug_color="#828482")
session.merge(stone)

dirt = Block(5, name="Dirt", solid=1, gravity=0, light_level=0, z=1, debug_color="#905D0B")
session.merge(dirt)

coal = Block(6, name="Coal", solid=1, gravity=0, light_level=0, z=1,  debug_color="#383838")
session.merge(coal)

iron = Block(7, name="Iron", solid=1, gravity=0, light_level=0, z=1, debug_color="#B8B8B8")
session.merge(iron)

gold = Block(8, name="Gold", solid=1, gravity=0, light_level=0, z=1, debug_color="#E1E31D")
session.merge(gold)

diamond = Block(9, name="Diamond", solid=1, gravity=0, light_level=0, z=1, debug_color="#21DFEC")
session.merge(diamond)

stone_background = Block(10, name="Stone Darken", solid=0, gravity=0, light_level=0, z=0, debug_color="#5B5B5B")
session.merge(stone_background)

player_upper = Block(11, name="SSU", solid=1, gravity=1, light_level=0, z=1, debug_color="#F2BB90")
session.merge(player_upper)

player_lower = Block(12, name="SSL", solid=1, gravity=1, light_level=0, z=1, debug_color="#0F399F")
session.merge(player_lower)

session.commit()