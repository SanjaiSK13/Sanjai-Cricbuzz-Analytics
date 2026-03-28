-- =============================================================
-- Cricbuzz LiveStats — Seed Data
-- Covers all 25 SQL practice queries
-- =============================================================

PRAGMA foreign_keys = ON;

-- =============================================================
-- TEAMS (20 international teams)
-- =============================================================
INSERT OR IGNORE INTO teams (team_id, team_name, country, format) VALUES
(1,  'India',              'India',        'All'),
(2,  'Australia',          'Australia',    'All'),
(3,  'England',            'England',      'All'),
(4,  'Pakistan',           'Pakistan',     'All'),
(5,  'South Africa',       'South Africa', 'All'),
(6,  'New Zealand',        'New Zealand',  'All'),
(7,  'West Indies',        'West Indies',  'All'),
(8,  'Sri Lanka',          'Sri Lanka',    'All'),
(9,  'Bangladesh',         'Bangladesh',   'All'),
(10, 'Afghanistan',        'Afghanistan',  'All'),
(11, 'Zimbabwe',           'Zimbabwe',     'All'),
(12, 'Ireland',            'Ireland',      'All'),
(13, 'Netherlands',        'Netherlands',  'All'),
(14, 'Scotland',           'Scotland',     'All'),
(15, 'UAE',                'UAE',          'T20I'),
(16, 'Namibia',            'Namibia',      'T20I'),
(17, 'Papua New Guinea',   'Papua New Guinea', 'T20I'),
(18, 'Oman',               'Oman',         'T20I'),
(19, 'Nepal',              'Nepal',        'T20I'),
(20, 'Kenya',              'Kenya',        'ODI');

-- =============================================================
-- VENUES (15 international grounds)
-- =============================================================
INSERT OR IGNORE INTO venues (venue_id, venue_name, city, country, capacity) VALUES
(1,  'Narendra Modi Stadium',      'Ahmedabad',     'India',       132000),
(2,  'Eden Gardens',               'Kolkata',       'India',        66000),
(3,  'Wankhede Stadium',           'Mumbai',        'India',        33000),
(4,  'M. Chinnaswamy Stadium',     'Bengaluru',     'India',        38000),
(5,  'MA Chidambaram Stadium',     'Chennai',       'India',        38000),
(6,  'Melbourne Cricket Ground',   'Melbourne',     'Australia',    100024),
(7,  'Sydney Cricket Ground',      'Sydney',        'Australia',    48000),
(8,  'Lords Cricket Ground',       'London',        'England',      30000),
(9,  'The Oval',                   'London',        'England',      25500),
(10, 'Headingley',                 'Leeds',         'England',      18350),
(11, 'National Stadium',           'Karachi',       'Pakistan',     34228),
(12, 'Gaddafi Stadium',            'Lahore',        'Pakistan',     27000),
(13, 'Newlands Cricket Ground',    'Cape Town',     'South Africa', 25000),
(14, 'SuperSport Park',            'Centurion',     'South Africa', 22000),
(15, 'Basin Reserve',              'Wellington',    'New Zealand',  11600);

-- =============================================================
-- SERIES (12 series including 2024)
-- =============================================================
INSERT OR IGNORE INTO series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches) VALUES
(1,  'ICC World Test Championship Final 2023',   'England',       'Test',   '2023-06-07', '2023-06-11', 1),
(2,  'India vs Australia Test Series 2023-24',   'India',         'Test',   '2023-11-09', '2024-01-07', 4),
(3,  'ICC Cricket World Cup 2023',               'India',         'ODI',    '2023-10-05', '2023-11-19', 48),
(4,  'India vs England Test Series 2024',        'India',         'Test',   '2024-01-25', '2024-03-11', 5),
(5,  'ICC T20 World Cup 2024',                   'West Indies',   'T20I',   '2024-06-01', '2024-06-29', 55),
(6,  'India vs Sri Lanka T20I Series 2024',      'India',         'T20I',   '2024-07-05', '2024-07-14', 3),
(7,  'England vs West Indies Test 2024',         'England',       'Test',   '2024-07-10', '2024-07-30', 3),
(8,  'Pakistan vs Bangladesh Test 2024',         'Pakistan',      'Test',   '2024-08-21', '2024-09-03', 2),
(9,  'Australia vs India Border-Gavaskar 2024-25','Australia',    'Test',   '2024-11-22', '2025-01-07', 5),
(10, 'India vs New Zealand Test 2024',           'India',         'Test',   '2024-10-16', '2024-11-01', 3),
(11, 'South Africa vs Sri Lanka ODI 2024',       'South Africa',  'ODI',    '2024-09-15', '2024-09-25', 3),
(12, 'ICC Champions Trophy 2025',                'Pakistan',      'ODI',    '2025-02-19', '2025-03-09', 15);

-- =============================================================
-- PLAYERS (40 players across teams)
-- =============================================================
INSERT OR IGNORE INTO players (player_id, full_name, team_id, playing_role, batting_style, bowling_style, date_of_birth, nationality) VALUES
-- India
(1,  'Rohit Sharma',         1, 'Batsman',        'Right-hand bat', 'Right-arm offbreak',          '1987-04-30', 'India'),
(2,  'Virat Kohli',          1, 'Batsman',        'Right-hand bat', 'Right-arm medium',            '1988-11-05', 'India'),
(3,  'Shubman Gill',         1, 'Batsman',        'Right-hand bat', 'Right-arm offbreak',          '1999-09-08', 'India'),
(4,  'KL Rahul',             1, 'Wicket-keeper',  'Right-hand bat', 'Right-arm offbreak',          '1992-04-18', 'India'),
(5,  'Hardik Pandya',        1, 'All-rounder',    'Right-hand bat', 'Right-arm fast-medium',       '1993-10-11', 'India'),
(6,  'Ravindra Jadeja',      1, 'All-rounder',    'Left-hand bat',  'Slow left-arm orthodox',      '1988-12-06', 'India'),
(7,  'Jasprit Bumrah',       1, 'Bowler',         'Right-hand bat', 'Right-arm fast',              '1993-12-06', 'India'),
(8,  'Ravichandran Ashwin',  1, 'All-rounder',    'Right-hand bat', 'Right-arm offbreak',          '1986-09-17', 'India'),
(9,  'Mohammed Shami',       1, 'Bowler',         'Right-hand bat', 'Right-arm fast-medium',       '1990-09-03', 'India'),
(10, 'Yashasvi Jaiswal',     1, 'Batsman',        'Left-hand bat',  'Slow left-arm orthodox',      '2001-12-28', 'India'),
-- Australia
(11, 'Steve Smith',          2, 'Batsman',        'Right-hand bat', 'Right-arm legbreak',          '1989-06-02', 'Australia'),
(12, 'David Warner',         2, 'Batsman',        'Left-hand bat',  'Right-arm offbreak',          '1986-10-27', 'Australia'),
(13, 'Pat Cummins',          2, 'All-rounder',    'Right-hand bat', 'Right-arm fast',              '1993-05-08', 'Australia'),
(14, 'Mitchell Starc',       2, 'Bowler',         'Left-hand bat',  'Left-arm fast',               '1990-01-30', 'Australia'),
(15, 'Travis Head',          2, 'Batsman',        'Left-hand bat',  'Right-arm offbreak',          '1993-12-29', 'Australia'),
(16, 'Marnus Labuschagne',   2, 'Batsman',        'Right-hand bat', 'Right-arm legbreak',          '1994-06-22', 'Australia'),
(17, 'Nathan Lyon',          2, 'Bowler',         'Right-hand bat', 'Right-arm offbreak',          '1987-11-20', 'Australia'),
-- England
(18, 'Joe Root',             3, 'Batsman',        'Right-hand bat', 'Right-arm offbreak',          '1990-12-30', 'England'),
(19, 'Ben Stokes',           3, 'All-rounder',    'Left-hand bat',  'Right-arm fast-medium',       '1991-06-04', 'England'),
(20, 'Stuart Broad',         3, 'Bowler',         'Right-hand bat', 'Right-arm fast-medium',       '1986-06-24', 'England'),
(21, 'James Anderson',       3, 'Bowler',         'Right-hand bat', 'Right-arm swing',             '1982-07-30', 'England'),
(22, 'Jonny Bairstow',       3, 'Wicket-keeper',  'Right-hand bat', 'Right-arm medium',            '1989-09-26', 'England'),
(23, 'Zak Crawley',          3, 'Batsman',        'Right-hand bat', 'Right-arm medium',            '1998-02-03', 'England'),
-- Pakistan
(24, 'Babar Azam',           4, 'Batsman',        'Right-hand bat', 'Right-arm offbreak',          '1994-10-15', 'Pakistan'),
(25, 'Shaheen Afridi',       4, 'Bowler',         'Left-hand bat',  'Left-arm fast',               '2000-04-06', 'Pakistan'),
(26, 'Mohammad Rizwan',      4, 'Wicket-keeper',  'Right-hand bat', 'Right-arm medium',            '1992-06-01', 'Pakistan'),
(27, 'Fakhar Zaman',         4, 'Batsman',        'Left-hand bat',  'Right-arm offbreak',          '1990-04-10', 'Pakistan'),
-- South Africa
(28, 'Kagiso Rabada',        5, 'Bowler',         'Right-hand bat', 'Right-arm fast',              '1995-05-25', 'South Africa'),
(29, 'Quinton de Kock',      5, 'Wicket-keeper',  'Left-hand bat',  'Right-arm medium',            '1992-12-17', 'South Africa'),
(30, 'Temba Bavuma',         5, 'Batsman',        'Right-hand bat', 'Right-arm medium',            '1990-05-17', 'South Africa'),
-- New Zealand
(31, 'Kane Williamson',      6, 'Batsman',        'Right-hand bat', 'Right-arm offbreak',          '1990-08-08', 'New Zealand'),
(32, 'Trent Boult',          6, 'Bowler',         'Right-hand bat', 'Left-arm fast-medium',        '1989-07-22', 'New Zealand'),
(33, 'Tim Southee',          6, 'Bowler',         'Right-hand bat', 'Right-arm fast-medium',       '1988-12-11', 'New Zealand'),
-- West Indies
(34, 'Nicholas Pooran',      7, 'Wicket-keeper',  'Left-hand bat',  'Right-arm offbreak',          '1995-10-02', 'West Indies'),
(35, 'Jason Holder',         7, 'All-rounder',    'Right-hand bat', 'Right-arm fast-medium',       '1991-11-05', 'West Indies'),
-- Sri Lanka
(36, 'Dimuth Karunaratne',   8, 'Batsman',        'Left-hand bat',  'Right-arm offbreak',          '1988-04-21', 'Sri Lanka'),
(37, 'Wanindu Hasaranga',    8, 'All-rounder',    'Right-hand bat', 'Right-arm legbreak',          '1997-07-29', 'Sri Lanka'),
-- Bangladesh
(38, 'Shakib Al Hasan',      9, 'All-rounder',    'Left-hand bat',  'Slow left-arm orthodox',      '1987-03-24', 'Bangladesh'),
-- Afghanistan
(39, 'Rashid Khan',         10, 'All-rounder',    'Right-hand bat', 'Right-arm legbreak',          '1998-09-20', 'Afghanistan'),
(40, 'Mohammad Nabi',       10, 'All-rounder',    'Right-hand bat', 'Right-arm offbreak',          '1985-01-01', 'Afghanistan');

-- =============================================================
-- BATTING STATS (career aggregates)
-- =============================================================
INSERT OR IGNORE INTO batting_stats (player_id, format, matches, innings, runs_scored, highest_score, batting_avg, strike_rate, centuries, half_centuries) VALUES
-- Rohit Sharma
(1,  'Test', 67,  111, 4301, 212, 40.58, 57.5,  12, 18),
(1,  'ODI',  264, 256, 10709,264, 48.67, 90.5,  31, 59),
(1,  'T20I', 159, 152, 4231, 118, 32.05, 139.8,  5, 32),
-- Virat Kohli
(2,  'Test', 123, 210, 9230, 254, 48.99, 55.8,  29, 30),
(2,  'ODI',  295, 283, 13848,183, 58.69, 93.4,  50, 72),
(2,  'T20I', 125, 114, 4188, 122, 52.35, 136.9, 1,  38),
-- Shubman Gill
(3,  'Test', 32,  58,  2400, 210, 44.44, 59.2,  6,  10),
(3,  'ODI',  64,  62,  3122, 208, 55.75, 100.8, 8,  17),
(3,  'T20I', 38,  38,  1320, 126, 40.12, 158.2, 3,   7),
-- KL Rahul
(4,  'Test', 53,  94,  2980, 199, 34.65, 50.8,  7,  13),
(4,  'ODI',  72,  65,  2213, 112, 46.44, 86.5,  3,  17),
(4,  'T20I', 72,  67,  2265, 110, 37.75, 136.4, 2,  23),
-- Hardik Pandya
(5,  'Test', 11,  16,  532,  108, 38.00, 67.0,  1,   2),
(5,  'ODI',  90,  75,  1938, 92,  32.30, 121.8, 0,  11),
(5,  'T20I', 105, 88,  1728, 87,  27.87, 146.2, 0,   8),
-- Ravindra Jadeja
(6,  'Test', 78,  110, 3088, 175, 36.02, 57.5,  3,  15),
(6,  'ODI',  196, 134, 2756, 87,  32.19, 91.8,  0,  13),
(6,  'T20I', 74,  51,  515,  46,  16.61, 119.9, 0,   0),
-- Jasprit Bumrah
(7,  'Test', 40,  49,  282,  55,  8.56,  52.0,  0,   1),
(7,  'ODI',  89,  30,  74,   19,  4.11,  72.0,  0,   0),
(7,  'T20I', 68,  8,   38,   10,  7.60,  95.0,  0,   0),
-- Ravichandran Ashwin
(8,  'Test', 106, 142, 3503, 124, 28.04, 53.2,  6,  14),
(8,  'ODI',  113, 75,  707,  65,  13.60, 78.1,  0,   2),
(8,  'T20I', 65,  19,  123,  31,  12.30, 107.9, 0,   0),
-- Mohammed Shami
(9,  'Test', 67,  86,  659,  56,  10.79, 55.0,  0,   1),
(9,  'ODI',  101, 32,  176,  25,  7.33,  79.0,  0,   0),
-- Yashasvi Jaiswal
(10, 'Test', 14,  25,  1478, 214, 63.39, 73.4,  4,   5),
(10, 'ODI',  4,   4,   105,  55,  35.00, 112.9, 0,   1),
(10, 'T20I', 28,  27,  1012, 100, 40.48, 167.8, 1,   8),
-- Steve Smith
(11, 'Test', 112, 194, 9286, 239, 56.01, 57.6,  32,  37),
(11, 'ODI',  145, 134, 5388, 164, 43.81, 85.2,  12,  33),
(11, 'T20I', 54,  52,  1360, 90,  28.33, 124.5, 0,   9),
-- David Warner
(12, 'Test', 112, 204, 8786, 335, 45.75, 72.1,  26,  37),
(12, 'ODI',  161, 157, 6932, 179, 45.30, 96.7,  22,  33),
(12, 'T20I', 100, 98,  3277, 100, 34.73, 141.7, 1,   24),
-- Pat Cummins
(13, 'Test', 59,  80,  1234, 87,  18.41, 65.2,  0,   4),
(13, 'ODI',  101, 55,  573,  50,  15.49, 110.8, 0,   1),
(13, 'T20I', 54,  27,  258,  43,  17.20, 138.0, 0,   0),
-- Joe Root
(18, 'Test', 146, 261, 13098,254, 54.34, 55.2,  35,  64),
(18, 'ODI',  171, 167, 6609, 133, 50.07, 88.0,  17,  56),
(18, 'T20I', 32,  30,  893,  90,  30.78, 124.2, 0,    4),
-- Ben Stokes
(19, 'Test', 105, 171, 6158, 258, 39.47, 58.6,  13,  28),
(19, 'ODI',  105, 88,  2928, 102, 40.67, 95.0,  3,   21),
-- Babar Azam
(24, 'Test', 55,  95,  4085, 196, 47.50, 52.3,  10,  21),
(24, 'ODI',  124, 119, 5741, 158, 59.18, 88.3,  20,  33),
(24, 'T20I', 120, 117, 4223, 122, 44.97, 129.0, 3,   39),
-- Shakib Al Hasan
(38, 'Test', 70,  122, 4819, 217, 39.50, 52.0,  10,  31),
(38, 'ODI',  247, 238, 7668, 134, 37.44, 82.1,  9,   54),
(38, 'T20I', 129, 118, 2468, 84,  22.85, 122.1, 0,   14),
-- Rashid Khan
(39, 'Test', 12,  15,  311,  72,  22.21, 65.5,  0,   2),
(39, 'ODI',  88,  70,  922,  60,  17.17, 94.6,  0,   4),
(39, 'T20I', 102, 71,  683,  48,  14.64, 150.5, 0,   2),
-- Kane Williamson
(31, 'Test', 102, 178, 8640, 251, 54.28, 52.0,  25,  38),
(31, 'ODI',  162, 156, 6985, 148, 47.52, 81.6,  14,  56),
(31, 'T20I', 91,  89,  2688, 95,  33.85, 119.8, 0,   22);

-- =============================================================
-- BOWLING STATS (career aggregates)
-- =============================================================
INSERT OR IGNORE INTO bowling_stats (player_id, format, matches, innings, overs_bowled, wickets_taken, runs_conceded, bowling_avg, economy_rate, best_bowling, five_wickets) VALUES
-- Jasprit Bumrah
(7,  'Test', 40,  72,  1580.5, 195, 4142, 21.24, 2.62, '6/27',  0),
(7,  'ODI',  89,  87,  840.4,  149, 4056, 27.22, 4.82, '5/27',  2),
(7,  'T20I', 68,  68,  246.0,  89,  1803, 20.26, 7.33, '4/14',  0),
-- Ravichandran Ashwin
(8,  'Test', 106, 192, 4489.5, 537, 12053,22.43, 2.68, '7/59', 37),
(8,  'ODI',  113, 109, 959.5,  156, 7120, 45.64, 7.42, '4/25',  0),
(8,  'T20I', 65,  63,  241.0,  72,  2153, 29.90, 8.93, '4/8',   0),
-- Ravindra Jadeja
(6,  'Test', 78,  140, 3178.4, 319, 7545, 23.65, 2.37, '7/48', 14),
(6,  'ODI',  196, 181, 1663.5, 225, 7843, 34.85, 4.71, '5/36',  2),
(6,  'T20I', 74,  67,  235.5,  54,  1958, 36.26, 8.30, '3/15',  0),
-- Mohammed Shami
(9,  'Test', 67,  122, 2258.2, 240, 6384, 26.60, 2.83, '7/74',  8),
(9,  'ODI',  101, 97,  892.2,  195, 5143, 26.37, 5.76, '5/69',  2),
-- Hardik Pandya
(5,  'ODI',  90,  75,  548.4,  89,  3295, 37.02, 6.00, '4/38',  0),
(5,  'T20I', 105, 83,  280.1,  83,  2332, 28.10, 8.32, '4/16',  0),
-- Stuart Broad
(20, 'Test', 167, 302, 5765.5, 604, 15425,25.54, 2.68, '8/15', 20),
-- James Anderson
(21, 'Test', 188, 341, 7216.0, 703, 17298,24.60, 2.40, '7/42', 31),
-- Pat Cummins
(13, 'Test', 59,  109, 2058.5, 247, 5786, 23.42, 2.81, '7/23', 10),
(13, 'ODI',  101, 96,  794.4,  183, 4162, 22.74, 5.24, '5/70',  3),
(13, 'T20I', 54,  53,  186.2,  68,  1621, 23.84, 8.70, '3/22',  0),
-- Mitchell Starc
(14, 'Test', 89,  162, 3342.5, 342, 9177, 26.83, 2.75, '6/50', 11),
(14, 'ODI',  124, 122, 1116.0, 237, 5836, 24.62, 5.23, '6/28',  5),
(14, 'T20I', 58,  58,  213.3,  74,  1817, 24.55, 8.51, '5/23',  1),
-- Nathan Lyon
(17, 'Test', 134, 249, 5555.2, 530, 14143,26.68, 2.55, '8/50', 21),
-- Kagiso Rabada
(28, 'Test', 58,  108, 2135.0, 273, 5912, 21.65, 2.77, '7/112', 11),
(28, 'ODI',  82,  78,  714.0,  150, 3819, 25.46, 5.35, '6/16',  3),
(28, 'T20I', 74,  74,  271.0,  113, 2341, 20.72, 8.64, '4/21',  0),
-- Trent Boult
(32, 'Test', 84,  153, 3069.0, 317, 8278, 26.11, 2.70, '6/32', 13),
(32, 'ODI',  105, 103, 956.3,  184, 4855, 26.38, 5.08, '5/21',  4),
(32, 'T20I', 72,  72,  262.4,  87,  2242, 25.77, 8.54, '4/21',  0),
-- Tim Southee
(33, 'Test', 106, 193, 3925.2, 390, 10598,27.17, 2.70, '7/64', 17),
-- Shakib Al Hasan
(38, 'Test', 70,  128, 2790.5, 242, 6813, 28.15, 2.44, '7/36', 19),
(38, 'ODI',  247, 232, 1910.5, 315, 9924, 31.50, 5.19, '5/29',  4),
(38, 'T20I', 129, 124, 463.5,  143, 3727, 26.06, 8.04, '5/20',  1),
-- Rashid Khan
(39, 'Test', 12,  23,  490.3,  58,  1186, 20.45, 2.42, '5/50',  5),
(39, 'ODI',  88,  85,  773.0,  176, 3416, 19.41, 4.42, '7/18', 10),
(39, 'T20I', 102, 100, 387.4,  145, 2773, 19.12, 7.15, '4/9',   0),
-- Mohammad Nabi
(40, 'ODI',  104, 97,  742.5,  92,  3567, 38.77, 4.80, '4/30',  0),
(40, 'T20I', 100, 95,  323.4,  78,  2614, 33.51, 8.07, '4/10',  0),
-- Wanindu Hasaranga
(37, 'Test', 10,  19,  352.3,  40,  1014, 25.35, 2.88, '5/57',  2),
(37, 'ODI',  75,  69,  566.2,  96,  3174, 33.06, 5.60, '6/28',  1),
(37, 'T20I', 76,  76,  278.1,  121, 2336, 19.30, 8.40, '6/19',  2);

-- =============================================================
-- FIELDING STATS
-- =============================================================
INSERT OR IGNORE INTO fielding_stats (player_id, catches, stumpings, run_outs) VALUES
(1, 45, 0, 15), (2, 78, 0, 22), (3, 28, 0, 8),  (4, 95, 18, 12),
(5, 32, 0, 9),  (6, 155,0, 18), (7, 18, 0, 5),  (8, 112,0, 10),
(9, 20, 0, 6),  (10,15, 0, 4),  (11,120,0, 25), (12,55, 0, 18),
(13,45, 0, 12), (14,35, 0, 8),  (15,62, 0, 14), (17,85, 0, 8),
(18,172,0, 25), (19,68, 0, 15), (20,45, 0, 10), (21,125,0, 12),
(22,185,28,18), (24,85, 0, 15), (25,22, 0, 6),  (26,210,35,14),
(28,35, 0, 8),  (29,195,42,16), (31,142,0, 22), (32,28, 0, 8),
(33,55, 0, 12), (34,88, 24,10), (35,52, 0, 18), (37,45, 0, 8),
(38,72, 0, 20), (39,48, 0, 12), (40,38, 0, 10);

-- =============================================================
-- MATCHES (30 completed matches + 2 live + 3 upcoming)
-- =============================================================
INSERT OR IGNORE INTO matches
(match_id, match_desc, team1_id, team2_id, venue_id, series_id, match_date, match_format,
 toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type, status) VALUES
-- Completed
(1,  'India vs Australia 1st Test',    1,2,  1,  2,  '2023-11-09','Test', 1,'bat',  2,'9 wickets','wickets','completed'),
(2,  'India vs Australia 2nd Test',    1,2,  2,  2,  '2023-12-06','Test', 2,'bowl', 1,'6 wickets','wickets','completed'),
(3,  'India vs Australia 3rd Test',    1,2,  5,  2,  '2023-12-14','Test', 1,'bat',  1,'8 wickets','wickets','completed'),
(4,  'India vs Australia 4th Test',    1,2,  4,  2,  '2024-01-26','Test', 2,'bat',  2,'100 runs','runs',   'completed'),
(5,  'India vs England 1st Test',      1,3,  5,  4,  '2024-01-25','Test', 3,'bat',  3,'28 runs', 'runs',   'completed'),
(6,  'India vs England 2nd Test',      1,3,  4,  4,  '2024-02-02','Test', 1,'bat',  1,'106 runs','runs',   'completed'),
(7,  'India vs England 3rd Test',      1,3,  2,  4,  '2024-02-15','Test', 3,'bowl', 1,'434 runs','runs',   'completed'),
(8,  'India vs England 4th Test',      1,3,  3,  4,  '2024-02-23','Test', 1,'bat',  3,'5 wickets','wickets','completed'),
(9,  'India vs England 5th Test',      1,3,  1,  4,  '2024-03-07','Test', 1,'bat',  1,'1 wicket','wickets','completed'),
(10, 'ICC WC 2023: India vs Pak',      1,4,  1,  3,  '2023-10-14','ODI',  1,'bat',  1,'7 wickets','wickets','completed'),
(11, 'ICC WC 2023: India vs NZ',       1,6,  3,  3,  '2023-10-22','ODI',  6,'bat',  1,'4 wickets','wickets','completed'),
(12, 'ICC WC 2023: India vs SA',       1,5,  1,  3,  '2023-11-05','ODI',  1,'bat',  1,'243 runs','runs',   'completed'),
(13, 'ICC WC 2023 Final: India vs Aus',1,2,  1,  3,  '2023-11-19','ODI',  1,'bat',  2,'6 wickets','wickets','completed'),
(14, 'T20 WC 2024: India vs Pak',      1,4,  8,  5,  '2024-06-09','T20I', 4,'bat',  1,'6 runs',  'runs',   'completed'),
(15, 'T20 WC 2024: India vs Aus',      1,2,  8,  5,  '2024-06-24','T20I', 2,'bat',  1,'24 runs', 'runs',   'completed'),
(16, 'T20 WC 2024 Final: India vs SA', 1,5,  6,  5,  '2024-06-29','T20I', 1,'bat',  1,'7 runs',  'runs',   'completed'),
(17, 'Ind vs NZ 1st Test 2024',        1,6,  2,  10, '2024-10-16','Test', 6,'bowl', 6,'8 wickets','wickets','completed'),
(18, 'Ind vs NZ 2nd Test 2024',        1,6,  4,  10, '2024-10-24','Test', 1,'bat',  6,'113 runs','runs',   'completed'),
(19, 'Ind vs NZ 3rd Test 2024',        1,6,  5,  10, '2024-11-01','Test', 6,'bat',  6,'25 runs', 'runs',   'completed'),
(20, 'AUS vs IND 1st Test BGT 2024',   2,1,  6,  9,  '2024-11-22','Test', 2,'bat',  2,'295 runs','runs',   'completed'),
(21, 'AUS vs IND 2nd Test BGT 2024',   2,1,  7,  9,  '2024-12-06','Test', 1,'bowl', 1,'295 runs','runs',   'completed'),
(22, 'AUS vs IND 3rd Test BGT 2024',   2,1,  1,  9,  '2024-12-14','Test', 2,'bat',  2,'184 runs','runs',   'completed'),
(23, 'AUS vs IND 4th Test BGT 2024',   2,1,  6,  9,  '2024-12-26','Test', 1,'bat',  1,'295 runs','runs',   'completed'),
(24, 'AUS vs IND 5th Test BGT 2024',   2,1,  7,  9,  '2025-01-03','Test', 2,'bowl', 2,'6 wickets','wickets','completed'),
(25, 'Eng vs WI 1st Test 2024',        3,7,  8,  7,  '2024-07-10','Test', 3,'bat',  3,'241 runs','runs',   'completed'),
(26, 'Pak vs Ban 1st Test 2024',       4,9,  11, 8,  '2024-08-21','Test', 9,'bat',  9,'10 wickets','wickets','completed'),
(27, 'SA vs SL 1st ODI 2024',          5,8,  13, 11, '2024-09-15','ODI',  5,'bat',  5,'50 runs', 'runs',   'completed'),
(28, 'ICC CT 2025: India vs Pak',      1,4,  11, 12, '2025-02-23','ODI',  1,'bat',  1,'6 wickets','wickets','completed'),
(29, 'ICC CT 2025: Aus vs Eng',        2,3,  12, 12, '2025-02-22','ODI',  3,'bat',  3,'44 runs', 'runs',   'completed'),
(30, 'ICC CT 2025: SA vs NZ',          5,6,  12, 12, '2025-02-24','ODI',  5,'bowl', 6,'4 wickets','wickets','completed'),
-- Live
(31, 'AUS vs NZ T20I',                 2,6,  7,  NULL,'2025-03-24','T20I', 2,'bat',  NULL,NULL,   NULL,     'live'),
(32, 'Ind vs SL T20I',                 1,8,  5,  NULL,'2025-03-24','T20I', 1,'bowl', NULL,NULL,   NULL,     'live'),
-- Upcoming
(33, 'ENG vs PAK 1st ODI',             3,4,  8,  NULL,'2025-03-26','ODI',  NULL,NULL,NULL,NULL,   NULL,     'upcoming'),
(34, 'SA vs AFG T20I',                 5,10, 13, NULL,'2025-03-27','T20I', NULL,NULL,NULL,NULL,   NULL,     'upcoming'),
(35, 'IND vs AUS 1st ODI',             1,2,  3,  NULL,'2025-03-28','ODI',  NULL,NULL,NULL,NULL,   NULL,     'upcoming');

-- =============================================================
-- INNINGS (per-innings batting records for Q13, Q15, Q16, Q19, Q23-25)
-- =============================================================
INSERT OR IGNORE INTO innings
(innings_id, match_id, player_id, innings_number, batting_position, runs_scored, balls_faced, strike_rate, fours, sixes, dismissed, dismissal_type, match_date) VALUES
-- Match 1 (India vs Australia 1st Test) — India 1st innings
(1,  1, 1,  1, 1, 131, 198, 66.2, 18, 2, 1, 'caught',   '2023-11-09'),
(2,  1, 10, 1, 2, 82,  130, 63.1, 11, 1, 1, 'lbw',      '2023-11-09'),
(3,  1, 2,  1, 3, 76,  145, 52.4, 8,  0, 1, 'caught',   '2023-11-09'),
(4,  1, 3,  1, 4, 55,  78,  70.5, 7,  1, 1, 'bowled',   '2023-11-09'),
(5,  1, 4,  1, 5, 23,  45,  51.1, 3,  0, 1, 'caught',   '2023-11-09'),
(6,  1, 5,  1, 6, 99,  120, 82.5, 12, 3, 1, 'caught',   '2023-11-09'),
(7,  1, 6,  1, 7, 70,  100, 70.0, 8,  2, 0, 'not out',  '2023-11-09'),
-- Match 2 (India vs Australia 2nd Test)
(8,  2, 2,  1, 3, 186, 310, 60.0, 22, 2, 1, 'caught',   '2023-12-06'),
(9,  2, 11, 2, 1, 121, 235, 51.5, 15, 0, 1, 'lbw',      '2023-12-06'),
(10, 2, 1,  1, 1, 36,  70,  51.4, 5,  0, 1, 'caught',   '2023-12-06'),
(11, 2, 10, 1, 2, 171, 261, 65.5, 25, 3, 1, 'caught',   '2023-12-06'),
-- Match 3
(12, 3, 2,  1, 3, 29,  65,  44.6, 3,  0, 1, 'caught',   '2023-12-14'),
(13, 3, 1,  1, 1, 73,  128, 57.0, 9,  1, 1, 'lbw',      '2023-12-14'),
(14, 3, 8,  1, 8, 105, 162, 64.8, 12, 3, 0, 'not out',  '2023-12-14'),
-- Match 5 (India vs England 1st Test)
(15, 5, 2,  2, 3, 45,  98,  45.9, 6,  0, 1, 'caught',   '2024-01-25'),
(16, 5, 10, 1, 2, 72,  108, 66.7, 10, 1, 1, 'caught',   '2024-01-25'),
(17, 5, 18, 1, 3, 122, 228, 53.5, 15, 0, 0, 'not out',  '2024-01-25'),
(18, 5, 19, 2, 5, 155, 198, 78.3, 20, 4, 1, 'caught',   '2024-01-25'),
-- Match 7 (India vs England 3rd Test) — big win
(19, 7, 2,  1, 3, 59,  110, 53.6, 7,  0, 1, 'bowled',   '2024-02-15'),
(20, 7, 8,  2, 8, 37,  64,  57.8, 4,  1, 1, 'caught',   '2024-02-15'),
-- Match 10 (India vs Pakistan WC ODI)
(21, 10,1,  1, 1, 86,  92,  93.5, 8,  3, 1, 'caught',   '2023-10-14'),
(22, 10,2,  1, 3, 122, 97,  125.8,12, 1, 0, 'not out',  '2023-10-14'),
(23, 10,24, 1, 1, 42,  55,  76.4, 5,  1, 1, 'caught',   '2023-10-14'),
-- Match 13 (WC Final India vs Australia)
(24, 13,2,  1, 3, 54,  63,  85.7, 6,  1, 1, 'caught',   '2023-11-19'),
(25, 13,11, 2, 1, 137, 128, 107.0,15, 4, 0, 'not out',  '2023-11-19'),
(26, 13,15, 2, 2, 137, 120, 114.2,15, 4, 0, 'not out',  '2023-11-19'),
-- Match 14 (T20 WC India vs Pakistan)
(27, 14,1,  1, 1, 57,  49,  116.3,6,  2, 1, 'caught',   '2024-06-09'),
(28, 14,24, 2, 1, 44,  43,  102.3,5,  1, 1, 'bowled',   '2024-06-09'),
-- Match 16 (T20 WC Final India vs SA)
(29, 16,1,  1, 1, 57,  47,  121.3,6,  2, 1, 'run out',  '2024-06-29'),
(30, 16,2,  1, 3, 76,  59,  128.8,8,  2, 0, 'not out',  '2024-06-29'),
-- Match 17 (India vs NZ 1st Test)
(31, 17,2,  1, 3, 70,  135, 51.9, 8,  0, 1, 'caught',   '2024-10-16'),
(32, 17,31, 1, 1, 0,   5,   0.0,  0,  0, 1, 'bowled',   '2024-10-16'),
(33, 17,31, 2, 1, 61,  98,  62.2, 7,  1, 0, 'not out',  '2024-10-16'),
-- Match 20 (BGT 1st Test Australia vs India)
(34, 20,11, 1, 1, 49,  120, 40.8, 6,  0, 1, 'lbw',      '2024-11-22'),
(35, 20,10, 1, 2, 161, 297, 54.2, 20, 3, 1, 'caught',   '2024-11-22'),
(36, 20,15, 1, 4, 145, 156, 92.9, 17, 5, 0, 'not out',  '2024-11-22'),
(37, 20,2,  2, 3, 36,  80,  45.0, 3,  0, 1, 'caught',   '2024-11-22'),
-- Match 21 (BGT 2nd Test)
(38, 21,10, 1, 2, 77,  140, 55.0, 9,  2, 1, 'caught',   '2024-12-06'),
(39, 21,2,  1, 3, 100, 165, 60.6, 12, 0, 0, 'not out',  '2024-12-06'),
(40, 21,11, 2, 1, 105, 230, 45.7, 13, 0, 1, 'lbw',      '2024-12-06'),
-- Match 22 (BGT 3rd Test)
(41, 22,16, 1, 3, 72,  156, 46.2, 8,  0, 1, 'caught',   '2024-12-14'),
(42, 22,3,  1, 4, 31,  55,  56.4, 4,  0, 1, 'caught',   '2024-12-14'),
-- Match 28 (CT 2025 India vs Pakistan)
(43, 28,1,  1, 1, 83,  88,  94.3, 9,  2, 1, 'caught',   '2025-02-23'),
(44, 28,2,  1, 3, 100, 107, 93.5, 10, 1, 0, 'not out',  '2025-02-23'),
(45, 28,24, 1, 1, 66,  79,  83.5, 7,  1, 1, 'lbw',      '2025-02-23'),
-- More recent 2024/2025 innings for Q16, Q19 (need many innings per player)
(46, 6,  2,  1, 3, 45,  85,  52.9, 5,  0, 1, 'caught',   '2024-02-02'),
(47, 6,  1,  1, 1, 12,  28,  42.9, 1,  0, 1, 'lbw',      '2024-02-02'),
(48, 8,  2,  2, 3, 0,   8,   0.0,  0,  0, 1, 'bowled',   '2024-02-23'),
(49, 8,  1,  2, 1, 103, 148, 69.6, 13, 2, 0, 'not out',  '2024-02-23'),
(50, 9,  2,  1, 3, 48,  98,  49.0, 5,  0, 1, 'caught',   '2024-03-07'),
(51, 9,  10, 1, 2, 214, 380, 56.3, 28, 5, 1, 'caught',   '2024-03-07'),
(52, 19, 2,  1, 3, 17,  40,  42.5, 2,  0, 1, 'lbw',      '2024-11-01'),
(53, 19, 31, 2, 1, 52,  98,  53.1, 6,  1, 1, 'caught',   '2024-11-01'),
(54, 23, 10, 1, 2, 82,  150, 54.7, 10, 1, 1, 'caught',   '2024-12-26'),
(55, 23, 2,  2, 3, 17,  38,  44.7, 2,  0, 1, 'bowled',   '2024-12-26'),
(56, 24, 2,  2, 3, 89,  170, 52.4, 10, 1, 1, 'caught',   '2025-01-03'),
(57, 24, 11, 1, 1, 140, 261, 53.6, 17, 2, 0, 'not out',  '2025-01-03'),
(58, 29, 18, 1, 3, 67,  78,  85.9, 8,  1, 1, 'caught',   '2025-02-22'),
(59, 29, 11, 1, 1, 88,  112, 78.6, 10, 2, 1, 'caught',   '2025-02-22'),
(60, 30, 31, 1, 1, 34,  55,  61.8, 4,  0, 1, 'lbw',      '2025-02-24');

-- =============================================================
-- BOWLING INNINGS (per-innings bowling for Q14, Q17, Q18, Q21)
-- =============================================================
INSERT OR IGNORE INTO bowling_innings
(bowling_innings_id, match_id, player_id, innings_number, overs_bowled, maidens, runs_conceded, wickets_taken, economy_rate, match_date) VALUES
-- Jasprit Bumrah across matches
(1,  1,  7,  2, 22.0, 4, 45, 3, 2.05, '2023-11-09'),
(2,  2,  7,  1, 24.0, 5, 52, 4, 2.17, '2023-12-06'),
(3,  3,  7,  2, 20.0, 3, 38, 5, 1.90, '2023-12-14'),
(4,  5,  7,  1, 18.0, 2, 55, 3, 3.06, '2024-01-25'),
(5,  7,  7,  2, 22.0, 4, 48, 4, 2.18, '2024-02-15'),
(6,  10, 7,  1, 10.0, 1, 40, 2, 4.00, '2023-10-14'),
(7,  11, 7,  1, 9.0,  0, 45, 1, 5.00, '2023-10-22'),
(8,  12, 7,  1, 9.0,  2, 27, 4, 3.00, '2023-11-05'),
(9,  13, 7,  1, 10.0, 1, 43, 2, 4.30, '2023-11-19'),
(10, 14, 7,  1, 4.0,  0, 14, 2, 3.50, '2024-06-09'),
(11, 16, 7,  1, 4.0,  1, 18, 2, 4.50, '2024-06-29'),
(12, 20, 7,  2, 25.0, 5, 57, 5, 2.28, '2024-11-22'),
(13, 21, 7,  1, 22.0, 3, 48, 4, 2.18, '2024-12-06'),
(14, 28, 7,  1, 10.0, 2, 33, 3, 3.30, '2025-02-23'),
-- Ravichandran Ashwin
(15, 1,  8,  2, 32.0, 6, 88, 6, 2.75, '2023-11-09'),
(16, 2,  8,  1, 28.5, 5, 72, 4, 2.50, '2023-12-06'),
(17, 5,  8,  1, 26.0, 4, 70, 3, 2.69, '2024-01-25'),
(18, 7,  8,  2, 42.0, 8, 95, 7, 2.26, '2024-02-15'),
(19, 17, 8,  1, 18.0, 3, 48, 2, 2.67, '2024-10-16'),
-- Ravindra Jadeja
(20, 2,  6,  2, 36.0, 7, 82, 5, 2.28, '2023-12-06'),
(21, 5,  6,  2, 28.0, 5, 65, 4, 2.32, '2024-01-25'),
(22, 9,  6,  1, 32.0, 6, 78, 5, 2.44, '2024-03-07'),
(23, 17, 6,  1, 22.0, 4, 58, 3, 2.64, '2024-10-16'),
-- Pat Cummins (at MCG and SCG)
(24, 13, 13, 1, 10.0, 2, 48, 2, 4.80, '2023-11-19'),
(25, 20, 13, 1, 22.0, 3, 65, 4, 2.95, '2024-11-22'),
(26, 21, 13, 2, 24.0, 4, 60, 5, 2.50, '2024-12-06'),
(27, 22, 13, 1, 20.0, 2, 55, 3, 2.75, '2024-12-14'),
(28, 24, 13, 1, 25.0, 5, 58, 6, 2.32, '2025-01-03'),
-- Mitchell Starc
(29, 20, 14, 2, 22.0, 3, 78, 3, 3.55, '2024-11-22'),
(30, 21, 14, 1, 18.0, 2, 55, 4, 3.06, '2024-12-06'),
(31, 24, 14, 2, 20.0, 4, 45, 5, 2.25, '2025-01-03'),
-- Nathan Lyon
(32, 20, 17, 1, 38.0, 7, 95, 4, 2.50, '2024-11-22'),
(33, 22, 17, 2, 44.0, 9,102, 5, 2.32, '2024-12-14'),
(34, 23, 17, 1, 40.0, 8, 88, 6, 2.20, '2024-12-26'),
-- Kagiso Rabada
(35, 12, 28, 1, 10.0, 1, 33, 3, 3.30, '2023-11-05'),
(36, 27, 28, 1, 10.0, 2, 38, 2, 3.80, '2024-09-15'),
-- Shaheen Afridi
(37, 10, 25, 1, 10.0, 1, 44, 2, 4.40, '2023-10-14'),
(38, 14, 25, 2, 4.0,  0, 22, 1, 5.50, '2024-06-09'),
(39, 28, 25, 1, 10.0, 1, 48, 1, 4.80, '2025-02-23'),
-- Rashid Khan
(40, 10, 39, 1, 10.0, 0, 38, 3, 3.80, '2023-10-14'),
(41, 14, 39, 1, 4.0,  0, 18, 2, 4.50, '2024-06-09'),
(42, 16, 39, 1, 4.0,  0, 14, 3, 3.50, '2024-06-29'),
-- Trent Boult
(43, 11, 32, 1, 9.0,  1, 42, 2, 4.67, '2023-10-22'),
(44, 13, 32, 2, 10.0, 1, 52, 1, 5.20, '2023-11-19');