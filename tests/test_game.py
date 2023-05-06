import pytest

from .fixtures import * 


def test_poly(four_character_game):
    game = four_character_game
    action_list = {
        'normal_amy|normal_bob': 60
        , 'introvert_cas|normal_amy': 30
        , 'extrovert_dan|normal_amy': 30
        , 'introvert_cas|normal_bob': 30
        , 'extrovert_dan|normal_bob': 30
        , 'extrovert_dan|introvert_cas': 0
        }
    res = game.compute_poly(action_list)
    assert res == {
        'normal_amy|normal_bob': 60
        , 'extrovert_dan|introvert_cas|normal_amy|normal_bob': 30
        , 'extrovert_dan|introvert_cas': 0
    }

def test_endgame_sort(four_character_game):
    four_character_game._set_initial_attraction()
    res_sort = four_character_game.get_sort()
    print(res_sort)
    assert res_sort == {
        'normal_amy|normal_bob': 60
        , 'extrovert_dan|introvert_cas|normal_amy|normal_bob': 30
        , 'extrovert_dan|introvert_cas': 0
    }