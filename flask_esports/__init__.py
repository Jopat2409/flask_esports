"""

TO IMPLEMENT:
    [ ] - Database operations
    [ ] - Custom db schemas by subclassing resources
    [ ] - Allow for secure sessions / option for API key generation
    [ ]
"""
from .source import SourceId

def set_endpoint_directory(dir_: str) -> None:
    from esports_api.config import Config
    Config.API_ENDPOINT_DIR = dir_

def set_debug(debug: bool) -> None:
    from esports_api.config import Config
    Config.DEBUG = debug

def set_testing(testing: bool) -> None:
    from esports_api.config import Config
    Config.TESTING = testing

def run() -> None:
    from esports_api.app import create_app
    app = create_app()
    app.run()

__all__ = [SourceId, set_endpoint_directory]
