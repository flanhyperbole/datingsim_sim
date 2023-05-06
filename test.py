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

## the tests

def test_charater_random(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda x: 'no')
    character = Character('gloob')
    assert character.stats.extraversion_intraversion in Stats.STATRANGE
    assert character.stats.openess_calculation in Stats.STATRANGE
    assert character.stats.emotion_intelligence in Stats.STATRANGE

def test_chatacter_set_stats(monkeypatch):
    inputs = iter(['yes', '-5', '0', '3'])
    monkeypatch.setattr('builtins.input', lambda x: next(inputs))
    character = Character('gloob')
    assert character.stats.extraversion_intraversion == -5
    assert character.stats.openess_calculation == 0
    assert character.stats.emotion_intelligence == 3

def test_statbar_display():
    statbar = Stats.statbar(3)
    assert statbar == '[.....||||..]'

def test_normals_have_equal_stats(normal_bob, normal_amy):
    for stat_compare in zip(normal_bob.stats.get_stat_iter(), normal_amy.stats.get_stat_iter()):
        assert stat_compare[0] == stat_compare[1]

def test_setup_attraction(four_character_game):
    four_character_game._set_initial_attraction()
    assert 'normal_amy' in four_character_game.characters['normal_bob'].attraction
    assert four_character_game.characters['normal_bob'].attraction['normal_amy'] == 30
    assert four_character_game.characters['introvert_cas'].attraction['extrovert_dan'] == 0
    assert four_character_game.characters['introvert_cas'].attraction['normal_amy'] == 15
     

