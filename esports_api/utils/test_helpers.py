from esports_api.app.resources import Player, Match

def assert_player(p1: Player, p2: Player) -> None:
    """Performs an assert for each of the attributes of the player class
    The same as running assert ==, except since each attribute has its own assert statement
    it should be easier to see where any issues are

    Args:
        p1 (Player): The first player to compare
        p2 (Player): The second player to compare
    """
    assert p1.source == p2.source
    assert p1.alias == p2.alias
    assert p1.forename == p2.forename
    assert p1.surname == p2.surname
    assert p1.avatar == p2.avatar
    assert p1.current_team == p2.current_team


def assert_match(m1: Match, m2: Match) -> None:
    """Performs an assert for each of the attributes of the match class
    The same as running assert ==, except since each attribute has its own assert statement
    it should be easier to see where any issues are

    Args:
        m1 (Match): The first match to compare
        m2 (Match): The second match to compare
    """
    assert m1.match == m2.match
    assert m1.event == m2.event
    assert m1.match_name == m2.match_name
    assert m1.teams == m2.teams
    assert m1.score == m2.score
    assert m1.match_epoch == m2.match_epoch
    assert m1.stats == m2.stats
