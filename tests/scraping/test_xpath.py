import pytest

from flask_esports.scraping import xpath as xp

@pytest.mark.parametrize("elem,root,kwargs,xpath", [
    ("div", '', {"class": "vm-stats-game "}, "//div[contains(@class, 'vm-stats-game ')]"),
    ("div", '', {"class": "vm-stats-game ", "data-game-id": "all"}, "//div[contains(@class, 'vm-stats-game ') and contains(@data-game-id, 'all')]"),
    ("div", xp.xpath("div", class_="vm-stats-game "), {"class": "vm-stats-game ", "data-game-id": "all"}, "//div[contains(@class, 'vm-stats-game ')]//div[contains(@class, 'vm-stats-game ') and contains(@data-game-id, 'all')]"),
])
def test_create_xpath(elem, root, kwargs, xpath):
    assert xp.xpath(elem, root, **kwargs) == xpath


@pytest.mark.parametrize("paths, xpath", [
    ([xp.xpath("div", class_="test")], "//div[contains(@class, 'test')]"),
    ([], ""),
    ([xp.xpath("div", class_="test"), xp.xpath("div", class_="child-test")], "//div[contains(@class, 'test')]//div[contains(@class, 'child-test')]")

])
def test_xpath_join(paths, xpath):
    assert xp.join(*paths) == xpath
