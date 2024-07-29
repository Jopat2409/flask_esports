import pytest
from contextlib import nullcontext


from flask_esports import Source, SourceId

@pytest.mark.parametrize("endpoint, valid", [
    (" /test", False), ("/test ", False), ("/test?", False), ("/test space", False), ("//test", False), ("", False), (" ", False), ("/ ", False),
    ("/test", True), ("/test-endpoint", True), ("/test_endpoint", True), ("/test1234endpoint", True), ("/", True)
])
def test_valid_endpoint(endpoint, valid):
    assert Source.is_valid_endpoint(endpoint) is valid

