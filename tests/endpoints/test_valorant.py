from flask_esports.app.valorant.routes import ValorantRoutes
from tests.helpers import assert_player, assert_match
from esports_api.source_id import SourceId
from flask_esports.app.resources import Player, Match

def test_scrape_player():
    zekken = Player(SourceId("valorant", 4004), "zekken", "Zachary", "Patrone", "//owcdn.net/img/6416956f0da1e.png", 2)
    zekken_test = ValorantRoutes.get_player(4004)

    assert_player(zekken, zekken_test)

    ritesh = Player(SourceId("valorant", 12002), "Ritesh13", None, None, "/img/base/ph/sil.png", None)
    ritesh_test = ValorantRoutes.get_player(12002)

    assert_player(ritesh, ritesh_test)

def test_get_player(client):

    response = client.get("/valorant/player/4004").json
    assert response["success"]

    player_data = response["data"]
    assert player_data.get("alias", None) == "zekken"
    assert player_data.get("current-team", None) == 2

def test_scrape_match():
    sen_100t = Match(SourceId("valorant", 314625), 2004, "Regular Season: Week 1", 2, 120, 2, 0, 1712531400.0, {659: {'rating': 1.32, 'ACS': 233, 'kills': 36, 'deaths': 25, 'assists': 17, 'KAST': 74, 'ADR': 158, 'HS': 34, 'FK': 4, 'FD': 3}, 9: {'rating': 1.22, 'ACS': 213, 'kills': 29, 'deaths': 28, 'assists': 35, 'KAST': 76, 'ADR': 127, 'HS': 25, 'FK': 4, 'FD': 4}, 729: {'rating': 1.21, 'ACS': 184, 'kills': 27, 'deaths': 21, 'assists': 12, 'KAST': 86, 'ADR': 128, 'HS': 26, 'FK': 2, 'FD': 2}, 1265: {'rating': 1.19, 'ACS': 198, 'kills': 30, 'deaths': 21, 'assists': 7, 'KAST': 71, 'ADR': 135, 'HS': 36, 'FK': 2, 'FD': 3}, 4004: {'rating': 0.97, 'ACS': 239, 'kills': 34, 'deaths': 32, 'assists': 8, 'KAST': 67, 'ADR': 150, 'HS': 25, 'FK': 8, 'FD': 10}, 4147: {'rating': 1.11, 'ACS': 247, 'kills': 40, 'deaths': 30, 'assists': 3, 'KAST': 74, 'ADR': 171, 'HS': 29, 'FK': 9, 'FD': 3}, 3880: {'rating': 0.99, 'ACS': 215, 'kills': 29, 'deaths': 33, 'assists': 16, 'KAST': 76, 'ADR': 147, 'HS': 32, 'FK': 3, 'FD': 6}, 796: {'rating': 0.89, 'ACS': 152, 'kills': 21, 'deaths': 29, 'assists': 9, 'KAST': 74, 'ADR': 106, 'HS': 34, 'FK': 3, 'FD': 2}, 601: {'rating': 0.86, 'ACS': 191, 'kills': 27, 'deaths': 32, 'assists': 8, 'KAST': 60, 'ADR': 120, 'HS': 24, 'FK': 4, 'FD': 4}, 604: {'rating': 0.44, 'ACS': 82, 'kills': 10, 'deaths': 32, 'assists': 12, 'KAST': 52, 'ADR': 58, 'HS': 14, 'FK': 3, 'FD': 5}})
    sen_100t_test = ValorantRoutes.get_match(314625)

    assert_match(sen_100t, sen_100t_test)

def test_scrape_player_matches():
    ValorantRoutes.get_player_matches(4004, page=1)
    assert 1==0
