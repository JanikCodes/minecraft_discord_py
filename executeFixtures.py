from Fixtures.blockFixture import *
from Fixtures.blockHasStatesFixture import *
from session import session

# this file auto persists the entities coming from the fixture modules.

# Get all variables from blockFixture module
block_variables = [var for var in globals().values() if isinstance(var, Block)]
for block in block_variables:
    session.merge(block)
session.commit()

# Get all variables from blockHasStatesFixture module
block_states_variables = [var for var in globals().values() if isinstance(var, BlockHasStates)]
for block_state in block_states_variables:
    session.merge(block_state)
session.commit()