import pytest

from flask_esports.api.source import DataSource

class TestSource(DataSource):

    test_attr = "hello"

    def get_player(player_id):
        return None

@pytest.mark.parametrize("thing,implemented", [
    ("get_player", True), ("get_team", False), ("get_skibid_rizz", False), ("test_attr", False)
])
def test_is_implemented(thing, implemented):
    assert DataSource.is_implemented(TestSource, thing) == implemented
    assert DataSource.is_implemented(TestSource(), thing) == implemented

@pytest.mark.parametrize("method,args,result", [
    ("get_player", (1,), None), ("get_player_matches", (1, 1), []), ("get_player_teams", (1,), []),
    ("get_team", (1,), None), ("get_team_matches", (1, 1), []), ("get_team_players", (1,), []),
    ("get_match", (1,), None),
    ("get_event", (1,), None), ("get_event_matches", (1,1), []), ("get_event_teams", (1,), [])
])
def test_default_methods(method, args, result):
    assert getattr(TestSource, method)(*args) == result
