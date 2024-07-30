"""

TO IMPLEMENT:
    [ ] - Database operations
    [ ] - Custom db schemas by subclassing resources
    [ ] - Allow for secure sessions / option for API key generation
    [ ]
"""

from .source import SourceId


def run() -> None:
    from flask_esports.app import create_app

    app = create_app()
    app.run()


__all__ = [SourceId]
