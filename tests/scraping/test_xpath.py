import pytest

from flask_esports.scraping import xpath as xp

@pytest.mark.parametrize("elem,root,kwargs,xpath", [
    ("div", '', {"class": "vm-stats-game "}, "//div[contains(@class, 'vm-stats-game ')]"),
    ("div", '', {"class": "vm-stats-game ", "data-game-id": "all"}, "//div[contains(@class, 'vm-stats-game ') and contains(@data-game-id, 'all')]"),
    ("div", xp.create_xpath("div", class_="vm-stats-game "), {"class": "vm-stats-game ", "data-game-id": "all"}, "//div[contains(@class_, 'vm-stats-game ')]//div[contains(@class, 'vm-stats-game ') and contains(@data-game-id, 'all')]"),
])
def test_create_xpath(elem, root, kwargs, xpath):
    assert xp.create_xpath(elem, root, **kwargs) == xpath
