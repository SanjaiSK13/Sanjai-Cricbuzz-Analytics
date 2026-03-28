
PRAGMA foreign_keys = ON;

-- -------------------------------------------------------------
-- 1. TEAMS
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS teams (
    team_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name   TEXT    NOT NULL UNIQUE,
    country     TEXT    NOT NULL,
    format      TEXT    CHECK(format IN ('Test','ODI','T20I','All')),
    created_at  TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 2. VENUES
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS venues (
    venue_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name  TEXT    NOT NULL,
    city        TEXT    NOT NULL,
    country     TEXT    NOT NULL,
    capacity    INTEGER DEFAULT 0,
    created_at  TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 3. SERIES
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS series (
    series_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name     TEXT    NOT NULL,
    host_country    TEXT    NOT NULL,
    match_type      TEXT    CHECK(match_type IN ('Test','ODI','T20I','Mixed')),
    start_date      TEXT    NOT NULL,
    end_date        TEXT,
    total_matches   INTEGER DEFAULT 0,
    created_at      TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 4. MATCHES
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matches (
    match_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    match_desc          TEXT    NOT NULL,
    team1_id            INTEGER NOT NULL REFERENCES teams(team_id),
    team2_id            INTEGER NOT NULL REFERENCES teams(team_id),
    venue_id            INTEGER NOT NULL REFERENCES venues(venue_id),
    series_id           INTEGER REFERENCES series(series_id),
    match_date          TEXT    NOT NULL,
    match_format        TEXT    CHECK(match_format IN ('Test','ODI','T20I')),
    toss_winner_id      INTEGER REFERENCES teams(team_id),
    toss_decision       TEXT    CHECK(toss_decision IN ('bat','bowl')),
    winning_team_id     INTEGER REFERENCES teams(team_id),
    victory_margin      TEXT,
    victory_type        TEXT    CHECK(victory_type IN ('runs','wickets','draw','tie','no result')),
    status              TEXT    CHECK(status IN ('upcoming','live','completed')) DEFAULT 'upcoming',
    created_at          TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 5. PLAYERS
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS players (
    player_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name       TEXT    NOT NULL,
    team_id         INTEGER REFERENCES teams(team_id),
    playing_role    TEXT    CHECK(playing_role IN ('Batsman','Bowler','All-rounder','Wicket-keeper')),
    batting_style   TEXT    CHECK(batting_style IN ('Right-hand bat','Left-hand bat')),
    bowling_style   TEXT,
    date_of_birth   TEXT,
    nationality     TEXT,
    created_at      TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 6. BATTING STATS (career aggregates per player per format)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS batting_stats (
    stat_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id       INTEGER NOT NULL REFERENCES players(player_id),
    format          TEXT    NOT NULL CHECK(format IN ('Test','ODI','T20I')),
    matches         INTEGER DEFAULT 0,
    innings         INTEGER DEFAULT 0,
    runs_scored     INTEGER DEFAULT 0,
    highest_score   INTEGER DEFAULT 0,
    batting_avg     REAL    DEFAULT 0.0,
    strike_rate     REAL    DEFAULT 0.0,
    centuries       INTEGER DEFAULT 0,
    half_centuries  INTEGER DEFAULT 0,
    fours           INTEGER DEFAULT 0,
    sixes           INTEGER DEFAULT 0,
    UNIQUE(player_id, format)
);

-- -------------------------------------------------------------
-- 7. BOWLING STATS (career aggregates per player per format)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bowling_stats (
    stat_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id       INTEGER NOT NULL REFERENCES players(player_id),
    format          TEXT    NOT NULL CHECK(format IN ('Test','ODI','T20I')),
    matches         INTEGER DEFAULT 0,
    innings         INTEGER DEFAULT 0,
    overs_bowled    REAL    DEFAULT 0.0,
    wickets_taken   INTEGER DEFAULT 0,
    runs_conceded   INTEGER DEFAULT 0,
    bowling_avg     REAL    DEFAULT 0.0,
    economy_rate    REAL    DEFAULT 0.0,
    best_bowling    TEXT,
    five_wickets    INTEGER DEFAULT 0,
    UNIQUE(player_id, format)
);

-- -------------------------------------------------------------
-- 8. INNINGS (per-innings batting performance)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS innings (
    innings_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id        INTEGER NOT NULL REFERENCES matches(match_id),
    player_id       INTEGER NOT NULL REFERENCES players(player_id),
    innings_number  INTEGER CHECK(innings_number IN (1,2,3,4)) DEFAULT 1,
    batting_position INTEGER DEFAULT 0,
    runs_scored     INTEGER DEFAULT 0,
    balls_faced     INTEGER DEFAULT 0,
    strike_rate     REAL    DEFAULT 0.0,
    fours           INTEGER DEFAULT 0,
    sixes           INTEGER DEFAULT 0,
    dismissed       INTEGER DEFAULT 1,   -- 1=out, 0=not out
    dismissal_type  TEXT,
    match_date      TEXT,
    created_at      TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 9. BOWLING INNINGS (per-innings bowling performance)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS bowling_innings (
    bowling_innings_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id            INTEGER NOT NULL REFERENCES matches(match_id),
    player_id           INTEGER NOT NULL REFERENCES players(player_id),
    innings_number      INTEGER CHECK(innings_number IN (1,2,3,4)) DEFAULT 1,
    overs_bowled        REAL    DEFAULT 0.0,
    maidens             INTEGER DEFAULT 0,
    runs_conceded       INTEGER DEFAULT 0,
    wickets_taken       INTEGER DEFAULT 0,
    economy_rate        REAL    DEFAULT 0.0,
    wides               INTEGER DEFAULT 0,
    no_balls            INTEGER DEFAULT 0,
    match_date          TEXT,
    created_at          TEXT    DEFAULT (datetime('now'))
);

-- -------------------------------------------------------------
-- 10. FIELDING STATS (career aggregates per player)
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fielding_stats (
    stat_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id   INTEGER NOT NULL REFERENCES players(player_id) UNIQUE,
    catches     INTEGER DEFAULT 0,
    stumpings   INTEGER DEFAULT 0,
    run_outs    INTEGER DEFAULT 0,
    created_at  TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_matches_date         ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format       ON matches(match_format);
CREATE INDEX IF NOT EXISTS idx_matches_status       ON matches(status);
CREATE INDEX IF NOT EXISTS idx_players_team         ON players(team_id);
CREATE INDEX IF NOT EXISTS idx_players_role         ON players(playing_role);
CREATE INDEX IF NOT EXISTS idx_batting_stats_player ON batting_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_batting_stats_format ON batting_stats(format);
CREATE INDEX IF NOT EXISTS idx_bowling_stats_player ON bowling_stats(player_id);
CREATE INDEX IF NOT EXISTS idx_bowling_stats_format ON bowling_stats(format);
CREATE INDEX IF NOT EXISTS idx_innings_match        ON innings(match_id);
CREATE INDEX IF NOT EXISTS idx_innings_player       ON innings(player_id);
CREATE INDEX IF NOT EXISTS idx_innings_date         ON innings(match_date);
CREATE INDEX IF NOT EXISTS idx_bowling_innings_match  ON bowling_innings(match_id);
CREATE INDEX IF NOT EXISTS idx_bowling_innings_player ON bowling_innings(player_id);
CREATE INDEX IF NOT EXISTS idx_venues_country       ON venues(country);
CREATE INDEX IF NOT EXISTS idx_series_start         ON series(start_date);