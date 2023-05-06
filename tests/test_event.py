import pytest

from datingsim_sim.main import *
from .test import *

@pytest.fixture
def mock_event(four_character_game):

    event = Event()
    event.name = "TEST EVENT: Study Session"
    event.desc = "In prepation for an upcoming test everyone decides to work together"
        
    event.desc_sabotage = "{self_name} sabboages"
    event.desc_success = "{self_name} learns a lot studying with {other_name}"
    event.desc_fail = "{self_name} is distracted and embarrased by {other_name}"
    event.desc_normal = "{self_name} and {other_name} feel prepared for their test"

    event.character_number = 0
    event.characters = None
    event.stat_affects = 'extraversion_intraversion'
    event.stat_amounts = (3, 1, 0)
    four_character_game._set_initial_attraction()
    print(four_character_game.characters)
    event.game = four_character_game

    return event

def test_set_affecting_characters(mock_event):
    mock_event.affecting_characters()
    assert len(mock_event.characters) > 0


def test_event_run(mock_event):
    mock_event.event_run()
    assert True
