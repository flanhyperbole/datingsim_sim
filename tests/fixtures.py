import pytest
from datingsim_sim.main import *

@pytest.fixture
def normal_amy():
    return Character.create_character_with_stats('normal_amy')  

@pytest.fixture
def normal_bob():
    return Character.create_character_with_stats('normal_bob')    

@pytest.fixture
def introvert_cas():  
    return Character.create_character_with_stats('introvert_cas', 5, 5, 5)

@pytest.fixture
def extrovert_dan():
    return Character.create_character_with_stats('extrovert_dan', -5, -5, -5)

@pytest.fixture
def four_character_game(normal_amy, normal_bob, introvert_cas, extrovert_dan):
    game = Game(False)
    game.characters[normal_amy.name] = normal_amy
    game.characters[normal_bob.name] = normal_bob
    game.characters[introvert_cas.name] = introvert_cas
    game.characters[extrovert_dan.name] = extrovert_dan
    return game