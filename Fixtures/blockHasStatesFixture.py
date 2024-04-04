from Classes import BlockHasStates
from Fixtures.blockFixture import air, grass, stone, dirt, coal, iron, gold, diamond, stone_background, player_upper, \
    player_lower, wooden_log, leave

air_default = BlockHasStates(id=1, block_id=air.id, sprite="air", state_active=0, state_direction=1)
grass_default = BlockHasStates(id=2, block_id=grass.id, sprite="grass_side", state_active=0, state_direction=1)
stone_default = BlockHasStates(id=3, block_id=stone.id, sprite="stone", state_active=0, state_direction=1)
dirt_default = BlockHasStates(id=4, block_id=dirt.id, sprite="dirt", state_active=0, state_direction=1)
coal_default = BlockHasStates(id=5, block_id=coal.id, sprite="coal_ore", state_active=0, state_direction=1)
iron_default = BlockHasStates(id=6, block_id=iron.id, sprite="iron_ore", state_active=0, state_direction=1)
gold_default = BlockHasStates(id=7, block_id=gold.id, sprite="gold_ore", state_active=0, state_direction=1)
diamond_default = BlockHasStates(id=8, block_id=diamond.id, sprite="diamond_ore", state_active=0, state_direction=1)
stone_background_default = BlockHasStates(id=9, block_id=stone_background.id, sprite="stone_background", state_active=0, state_direction=1)
player_upper_right = BlockHasStates(id=10, block_id=player_upper.id, sprite="player_upper_right", state_active=0, state_direction=1)
player_upper_left = BlockHasStates(id=11, block_id=player_upper.id, sprite="player_upper_left", state_active=0, state_direction= -1)
player_lower_right = BlockHasStates(id=12, block_id=player_lower.id, sprite="player_lower_default", state_active=0, state_direction=1)
player_lower_left = BlockHasStates(id=13, block_id=player_lower.id, sprite="player_lower_default", state_active=0, state_direction= -1)
wooden_log_default = BlockHasStates(id=14, block_id=wooden_log.id, sprite="log_oak", state_active=0, state_direction=1)
leave_default = BlockHasStates(id=15, block_id=leave.id, sprite="leaves_oak", state_active=0, state_direction=1)
