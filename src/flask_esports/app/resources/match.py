from __future__ import annotations

from ...source import SourceId


class Match:
    TABLENAME = "matches"

    def __init__(
        self,
        match_id: SourceId,
        event_id: int,
        match_name: str,
        home_team: int,
        away_team: int,
        home_score: int,
        away_score: int,
        match_epoch: float,
        match_stats: dict,
    ) -> None:
        self.match = match_id
        self.event = event_id
        self.match_name = match_name
        self.teams = (home_team, away_team)
        self.score = (home_score, away_score)
        self.match_epoch = match_epoch
        self.stats = match_stats

    def __repr__(self) -> str:
        return f"{self.match_name}: {self.teams[0]}({self.score[0]}) vs {self.teams[1]}({self.score[1]})"

    def to_dict(self) -> dict:
        return {
            "match-id": self.match.get_id(),
            "event-id": self.event,
            "match-name": self.match_name,
            "match-date": self.match_epoch,
            "teams": [
                {"team-id": team, "score": self.score[i]}
                for i, team in enumerate(self.teams)
            ],
            "match-stats": self.stats,
        }

    @staticmethod
    def from_record(record: dict) -> Match:
        return record

    def to_record(self) -> tuple:
        return (
            self.match.get_source(),
            self.match.get_id(),
            self.event,
            self.match_name,
            self.match_epoch,
        )

    def __eq__(self, other: Match) -> bool:
        return (
            self.match == other.match
            and self.event == other.event
            and self.match_name == other.match_name
            and self.teams == other.teams
            and self.score == other.score
            and self.match_epoch == other.match_epoch
            and self.stats == other.stats
        )
