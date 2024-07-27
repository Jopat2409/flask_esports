import os

from esports_api.source import Source
from esports_api.source_id import SourceId

def set_endpoint_directory(dir_: str) -> None:
    from esports_api.config import Config
    Config.API_ENDPOINT_DIR = dir_

def run() -> None:
    from esports_api.app import create_app
    app = create_app()
    app.run()

__all__ = [Source, SourceId, set_endpoint_directory]
