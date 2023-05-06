from datingsim_sim.main import *

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
