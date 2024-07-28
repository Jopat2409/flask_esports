from esports_api import Source, SourceId

def test_source():

    test_basic = Source("tf2", [], False)
    assert test_basic.get_endpoint() == "/tf2"
    assert test_basic.sources == ["tf2"]
    assert test_basic.get_querystring() == 'source = "tf2"'

    test_suffixes = Source("valorant", ["vlr", "spikegg"], False)
    assert test_suffixes.get_endpoint() == "/valorant"
    assert test_suffixes.sources == ["valorant_vlr", "valorant_spikegg"]
    assert test_suffixes.get_querystring() == 'source IN ["valorant_vlr", "valorant_spikegg"]'

    test_root = Source("league", [], True)
    assert test_root.get_endpoint() == "/"
    assert test_root.sources == ["league"]
    assert test_root.get_querystring() == 'source = "league"'
