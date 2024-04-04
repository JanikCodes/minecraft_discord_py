from Fixtures.blockFixture import air, grass, stone, dirt, coal, iron, gold, diamond, stone_background, player_upper, \
    player_lower, wooden_log, leave
from Fixtures.blockHasStatesFixture import air_default, stone_default, dirt_default, grass_default, coal_default, \
    gold_default, iron_default, diamond_default, stone_background_default, player_upper_right, player_upper_left, \
    player_lower_right, player_lower_left, wooden_log_default, leave_default

from session import session

session.merge(air)
session.merge(grass)
session.merge(stone)
session.merge(dirt)
session.merge(coal)
session.merge(iron)
session.merge(gold)
session.merge(diamond)
session.merge(stone_background)
session.merge(player_upper)
session.merge(player_lower)
session.merge(wooden_log)
session.merge(leave)
session.commit()

session.merge(air_default)
session.merge(grass_default)
session.merge(stone_default)
session.merge(dirt_default)
session.merge(coal_default)
session.merge(iron_default)
session.merge(gold_default)
session.merge(diamond_default)
session.merge(stone_background_default)
session.merge(player_upper_right)
session.merge(player_upper_left)
session.merge(player_lower_right)
session.merge(player_lower_left)
session.merge(wooden_log_default)
session.merge(leave_default)
session.commit()