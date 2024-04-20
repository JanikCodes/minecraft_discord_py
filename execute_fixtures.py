from sqlalchemy.orm import sessionmaker

from Fixtures.block_fixture import *
from Fixtures.block_has_states_fixture import *
from database import engine

Session = sessionmaker(bind=engine)
session = Session()

# this file auto persists the entities coming from the fixture modules.
try:
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

except Exception as e:
    # rollback the transaction if an error occurs
    session.rollback()
    raise e
finally:
    # close the session
    session.close()