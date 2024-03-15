-- Drop the users table if it already exists to avoid conflicts when creating it anew
DROP TABLE IF EXISTS users;

-- Create the users table
-- This table holds the information of all users in the system
-- Every example online says storing images in databases is retarded (BLOBs) so im going to avoid doing that
CREATE TABLE users
(
    user_id     TEXT PRIMARY KEY, 
    password    TEXT NOT NULL,     
    first_name  TEXT(25),          
    last_name   TEXT(25),          
    age         DATE,              
    gender      TEXT DEFAULT 'Other', 
    bio         TEXT(255)          
);

-- This table stores the messages sent between users
CREATE TABLE messages
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT, 
    sender_id   TEXT,          
    receiver_id TEXT,          
    message     TEXT(255),     
    timesent    DATETIME DEFAULT CURRENT_TIME 
);

-- This table for bios
CREATE TABLE bios
(
    b_id    INTEGER PRIMARY KEY AUTOINCREMENT, 
    bio_id  TEXT,          
    bio     TEXT(255)      
);
