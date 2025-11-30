
CREATE TABLE teams (
    team_id INT PRIMARY KEY,
    team_name VARCHAR(100),
    country VARCHAR(50)
);

CREATE TABLE venues (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    capacity INT
);

CREATE TABLE players (
    player_id INT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50), -- Batsman, Bowler, etc.
    batting_style VARCHAR(50),
    bowling_style VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    series_name VARCHAR(100),
    match_type VARCHAR(20), -- Test, ODI, T20
    match_date DATE,
    venue_id INT,
    team1_id INT,
    team2_id INT,
    winner_id INT,
    toss_winner_id INT,
    toss_decision VARCHAR(10), -- 'BAT' or 'BOWL'
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);

CREATE TABLE player_performance (
    performance_id AUTO_INCREMENT PRIMARY KEY, -- or SERIAL for Postgres
    match_id INT,
    player_id INT,
    team_id INT,
    runs_scored INT,
    balls_faced INT,
    fours INT,
    sixes INT,
    wickets INT,
    overs_bowled DECIMAL(3,1),
    runs_conceded INT,
    catches INT,
    is_captain BOOLEAN,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
