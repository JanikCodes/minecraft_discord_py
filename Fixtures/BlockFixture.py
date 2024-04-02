from Classes import Block
from session import session

air = Block(1, name="Air", solid=0, gravity=0, light_level=10, z=0, image="air", debug_color="#0096FF")
session.merge(air)

grass = Block(2, name="Grass", solid=1, gravity=0, light_level=0, z=1, image="grass_side", debug_color="#32B32B")
session.merge(grass)

stone = Block(3, name="Stone", solid=1, gravity=0, light_level=0, z=1, image="stone", debug_color="#828482")
session.merge(stone)

sand = Block(4, name="Sand", solid=1, gravity=1, light_level=0, z=1, image="sand", debug_color="#F2DA28")
session.merge(sand)

dirt = Block(5, name="Dirt", solid=1, gravity=0, light_level=0, z=1, image="dirt", debug_color="#905D0B")
session.merge(dirt)

coal = Block(6, name="Coal", solid=1, gravity=0, light_level=0, z=1, image="coal_ore", debug_color="#383838")
session.merge(coal)

iron = Block(7, name="Iron", solid=1, gravity=0, light_level=0, z=1, image="iron_ore", debug_color="#B8B8B8")
session.merge(iron)

gold = Block(8, name="Gold", solid=1, gravity=0, light_level=0, z=1, image="gold_ore", debug_color="#E1E31D")
session.merge(gold)

diamond = Block(9, name="Diamond", solid=1, gravity=0, light_level=0, z=1, image="diamond_ore", debug_color="#21DFEC")
session.merge(diamond)

stone_darken = Block(10, name="Stone Darken", solid=0, gravity=0, light_level=0, z=0, image="stone_darken", debug_color="#5B5B5B")
session.merge(stone_darken)

steve_straight_upper = Block(11, name="SSU", solid=1, gravity=1, light_level=0, z=1, image="steve_straight_upper", debug_color="#F2BB90")
session.merge(steve_straight_upper)

steve_straight_lower = Block(12, name="SSL", solid=1, gravity=1, light_level=0, z=1, image="steve_straight_lower", debug_color="#0F399F")
session.merge(steve_straight_lower)

session.commit()