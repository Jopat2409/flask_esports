from __future__ import annotations
import time

from esports_api.source import SourceId

class Player:

    TABLENAME = "players"

    def __init__(self, source_id: SourceId, alias: str, forename: str, surname: str, avatar: str, current_team: int) -> None:
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
            "current-team": self.current_team
        }

    def load_additional_info(self, data: dict) -> None:
        """Loads additional data stored in the database. Override this method if you want to store additional
        json data for a specific game's player class

        Args:
            data (dict): The data pulled from the database
        """
        return

    @staticmethod
    def from_record(record: dict) -> Player:
        print(record)
        player = Player(
            SourceId(record["source"], record["player_id"]),
            record["alias"],
            record["forename"],
            record["surname"],
            record["avatar"],
            0
        )
        player.load_additional_info(record["additional_data"])
        return player

    def to_record(self) -> tuple:
        return (self.source.get_source(), self.source.get_id(), self.alias, self.forename, self.surname, self.avatar, time.time())

    def __eq__(self, other: Player) -> bool:
        return self.source == other.source and\
                self.alias == other.alias and\
                self.forename == other.forename and\
                self.surname == other.surname and\
                self.avatar == other.avatar and\
                self.current_team == other.current_team


    def __repr__(self) -> str:
        return f"Player {self.alias} ({self.forename} {self.surname}) {self.avatar} {self.current_team} {self.source}"

class PlayerTeamAssociation:

    TABLENAME = "player_team_association"

    def __init__(self, player_id: SourceId, team: SourceId, joined_at: float, left_at: float | None) -> None:
        self.player_id = player_id
        self.team_id = team
        self.joined_at = joined_at
        self.left_at = left_at

    @staticmethod
    def from_record(record: dict) -> PlayerTeamAssociation:
        return record

class PlayerMatchAssociation:

    TABLENAME = "player_match_assocation"

    def __init__(self, player_id: SourceId, match_id: SourceId):

        self.player = player_id
        self.match = match_id

    @staticmethod
    def from_record(record: dict) -> PlayerMatchAssociation:
        return record
