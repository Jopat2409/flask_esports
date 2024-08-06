from __future__ import annotations

from ..source import SourceId


class Player:
    """Contains all the information that can be represented"""

    def __init__(
        self,
        source_id: SourceId,
        alias: str,
        forename: str,
        surname: str,
        avatar: str,
        current_team: int,
    ) -> None:
        self.source = source_id
        self.alias = alias
        self.forename = forename
        self.surname = surname
        self.avatar = avatar
        self.current_team = int(current_team or 0) or None

    def to_dict(self) -> dict:
        return {
            "alias": self.alias,
            "forename": self.forename,
            "surname": self.surname,
            "avatar": self.avatar,
            "current-team": self.current_team,
        }

    def load_additional_info(self, data: dict) -> None:
        """Loads additional data stored in the database. Override this method if you want to store additional
        json data for a specific game's player class

        Args:
            data (dict): The data pulled from the database
        """
        return

    def __eq__(self, other: Player) -> bool:
        return (
            self.source == other.source
            and self.alias == other.alias
            and self.forename == other.forename
            and self.surname == other.surname
            and self.avatar == other.avatar
            and self.current_team == other.current_team
        )

    def __repr__(self) -> str:
        return f"Player {self.alias} ({self.forename} {self.surname}) {self.avatar} {self.current_team} {self.source}"
