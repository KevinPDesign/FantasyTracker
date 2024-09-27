-- Active: 1727372072972@@127.0.0.1@3306@fantasy_tracker
-- Create the 'players' table to store player data
CREATE TABLE IF NOT EXISTS players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique player identifier
    name VARCHAR(255) NOT NULL,                -- Full name of the player
    position VARCHAR(10) NOT NULL,             -- Player's position (e.g., QB, WR)
    team VARCHAR(50) NOT NULL                  -- Player's team (e.g., SF, NE)
);

-- Create the 'weekly_points' table to store weekly performance data
CREATE TABLE IF NOT EXISTS weekly_points (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique row identifier for each record
    player_id INT,                      -- Foreign key to reference 'players' table
    week_number INT NOT NULL,           -- The NFL week (1 to 18)
    points_made DECIMAL(5, 2),          -- Points made in the week
    points_proj DECIMAL(5, 2),          -- Projected points for the week
    opponent VARCHAR(50),               -- Opposing team for the week
    FOREIGN KEY (player_id) REFERENCES players(player_id)  -- Establishes relationship with 'players' table
);

ALTER TABLE weekly_points DROP PRIMARY KEY;


-- Modify the weekly_points table if needed
ALTER TABLE weekly_points 
    MODIFY COLUMN opponent VARCHAR(3),         -- Ensure opponent is a 3-character abbreviation
    ADD CONSTRAINT PK_weekly_points PRIMARY KEY (week, player_id);  -- Composite primary key

ALTER TABLE weekly_points 
ADD UNIQUE INDEX unique_week_player (player_id, week_number);

ALTER TABLE weekly_points 
ADD CONSTRAINT fk_player_id FOREIGN KEY (player_id) 
REFERENCES players(player_id) ON DELETE CASCADE;

DESCRIBE weekly_points;

SHOW INDEX FROM weekly_points;
SHOW CREATE TABLE weekly_points;
ALTER TABLE players MODIFY position VARCHAR(50) DEFAULT 'Unknown';
ALTER TABLE players MODIFY team VARCHAR(50) DEFAULT 'Unknown';
