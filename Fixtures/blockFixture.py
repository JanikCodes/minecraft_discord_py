from Classes import Block

# add new blocks below. Each block requires atleast one blockHasStates entity to render.

air = Block(1, name="Air", solid=False, gravity=False, light_level=10, z=0, debug_color="#0096FF")
grass = Block(2, name="Grass", solid=True, gravity=False, light_level=0, z=1, debug_color="#32B32B")
stone = Block(3, name="Stone", solid=True, gravity=False, light_level=0, z=1, debug_color="#828482")
dirt = Block(5, name="Dirt", solid=True, gravity=False, light_level=0, z=1, debug_color="#905D0B")
coal = Block(6, name="Coal", solid=True, gravity=False, light_level=0, z=1,  debug_color="#383838")
iron = Block(7, name="Iron", solid=True, gravity=False, light_level=0, z=1, debug_color="#B8B8B8")
gold = Block(8, name="Gold", solid=True, gravity=False, light_level=0, z=1, debug_color="#E1E31D")
diamond = Block(9, name="Diamond", solid=True, gravity=False, light_level=0, z=1, debug_color="#21DFEC")
stone_background = Block(10, name="Stone Darken", solid=False, gravity=False, light_level=0, z=0, debug_color="#5B5B5B")
player_upper = Block(11, name="SSU", solid=True, gravity=True, light_level=0, z=1, debug_color="#F2BB90")
player_lower = Block(12, name="SSL", solid=True, gravity=True, light_level=0, z=1, debug_color="#0F399F")
wooden_log = Block(13, name="Wooden Log", solid=True, gravity=False, light_level=0, z=1, debug_color="#A25013")
leave = Block(14, name="Leave", solid=True, gravity=False, light_level=0, z=1, debug_color="#269610")