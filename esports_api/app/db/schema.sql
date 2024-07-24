CREATE TABLE players (
    source VARCHAR,
    player_id INTEGER,
    alias VARCHAR,
    forename VARCHAR,
    surname VARCHAR,
    avatar VARCHAR,

    additional_data BLOB,
    last_fetched float,

    PRIMARY KEY (source, player_id)
);

CREATE TABLE matches (
    source VARCHAR,
    match_id INTEGER,

    event_id INTEGER,
    match_name VARCHAR,
    match_date FLOAT,

    PRIMARY KEY (source, match_id)
);

CREATE TABLE teams (
    source VARCHAR,
    team_id INTEGER,

    team_name VARCHAR,
    team_tag VARCHAR,
    logo VARCHAR,

    PRIMARY KEY (source, team_id)
);

CREATE TABLE match_team_association (
    source VARCHAR,
    match_id INTEGER,
    team_id INTEGER,

    score INTEGER,
    additional_data BLOB,

    PRIMARY KEY (source, match_id, team_id),
    FOREIGN KEY (source, match_id) REFERENCES matches (source, match_id)
    FOREIGN KEY (source, team_id) REFERENCES teams (source, team_id)
);

CREATE TABLE player_team_association (
    source VARCHAR,
    player_id INTEGER,
    team_id INTEGER,

    joined_at FLOAT,
    left_at FLOAT,

    PRIMARY KEY (source, player_id, team_id, joined_at),
    FOREIGN KEY (source, player_id) REFERENCES players (source, player_id)
    FOREIGN KEY (source, team_id) REFERENCES teams (source, team_id)
)
