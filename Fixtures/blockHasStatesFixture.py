from Classes import BlockHasStates
from Fixtures.blockFixture import air, grass, stone, dirt, coal, iron, gold, diamond, stone_background, player_upper, \
    player_lower, wooden_log, leave, wooden_planks, sand, furnace, melon, bookshelf, crafting_table, ladder, stone_brick, tnt, torch, \
    brick, cobblestone, world_spawn

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
wooden_planks_default = BlockHasStates(id=16, block_id=wooden_planks.id, sprite="planks_oak", state_active=0, state_direction=1)
sand_default = BlockHasStates(id=17, block_id=sand.id, sprite="sand", state_active=0, state_direction=1)
furnace_default = BlockHasStates(id=18, block_id=furnace.id, sprite="furnace_front_off", state_active=0, state_direction=1)
melon_default = BlockHasStates(id=19, block_id=melon.id, sprite="melon_side", state_active=0, state_direction=1)
bookshelf_default = BlockHasStates(id=20, block_id=bookshelf.id, sprite="bookshelf", state_active=0, state_direction=1)
crafting_table_default = BlockHasStates(id=21, block_id=crafting_table.id, sprite="crafting_table_front", state_active=0, state_direction=1)
ladder_default = BlockHasStates(id=22, block_id=ladder.id, sprite="ladder", state_active=0, state_direction=1)
stonebrick_default = BlockHasStates(id=23, block_id=stone_brick.id, sprite="stonebrick", state_active=0, state_direction=1)
tnt_default = BlockHasStates(id=24, block_id=tnt.id, sprite="tnt_side", state_active=0, state_direction=1)
torch_default = BlockHasStates(id=25, block_id=torch.id, sprite="torch_on", state_active=0, state_direction=1)
brick_default = BlockHasStates(id=26, block_id=brick.id, sprite="brick", state_active=0, state_direction=1)
cobblestone_default = BlockHasStates(id=27, block_id=cobblestone.id, sprite="cobblestone", state_active=0, state_direction=1)
world_spawn_default = BlockHasStates(id=28, block_id=world_spawn.id, sprite="daylight_detector_inverted_top", state_active=0, state_direction=1)
