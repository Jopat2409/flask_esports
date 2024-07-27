from esports_api.app.resources import Player
from esports_api.app.db.query_factory import BasicQuery, LimitedQuery

def test_basic_query():
    q = BasicQuery(Player, "valorant", player_id=10)
    assert q.query == "SELECT * FROM players WHERE source_id = ? and player_id = ?;"
    assert q.args == ("valorant", 10)

    q = BasicQuery(Player, "valorant", player_id=10, alias="zekken", forename="Peter")
    assert q.query == "SELECT * FROM players WHERE source_id = ? and player_id = ? and alias = ? and forename = ?;"
    assert q.args == ("valorant", 10, "zekken", "Peter")

def test_limited_query():
    q = LimitedQuery(Player, "valorant", ["alias"], player_id=10)
    assert q.query == "SELECT players.alias FROM players WHERE source_id = ? and player_id = ?;"
    assert q.args == ("valorant", 10)

    q = LimitedQuery(Player, "valorant", ["alias", "forename", "surname"], player_id=10)
    assert q.query == "SELECT players.alias, players.forename, players.surname FROM players WHERE source_id = ? and player_id = ?;"
    assert q.args == ("valorant", 10)

    q = LimitedQuery(Player, "valorant", [("alias", "playerName"), "forename", "surname"], player_id=19)
    assert q.query == "SELECT players.alias as playerName, players.forename, players.surname FROM players WHERE source_id = ? and player_id = ?;"
    assert q.args == ("valorant", 19)
