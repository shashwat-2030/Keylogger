create database keylogger;
use keylogger;
SHOW TABLES;

-- table to store text
CREATE TABLE keystrokes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    key_pressed VARCHAR(50),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- table to store screenshots 
CREATE TABLE SCREENSHOT(SSID INTEGER AUTO_INCREMENT, Filename VARCHAR(255) NOT NULL,
IMAGE LONGBLOB NOT NULL, UPLOAD_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(SSID, Filename));

-- table to store audio files 
CREATE TABLE AUDIO(ADID INTEGER AUTO_INCREMENT, Filename VARCHAR(255) NOT NULL,
AUDIO_DATA LONGBLOB NOT NULL, UPLOAD_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(ADID, Filename));

-- table to store system information 
CREATE TABLE SYSTEM_INFO(Parameter VARCHAR(255), Value TEXT);

-- table to store system video
CREATE TABLE video (
    VID INT AUTO_INCREMENT PRIMARY KEY,
    Filename VARCHAR(255),
    Filepath TEXT,
    UPLOAD_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from video;
select * from screenshot;
select * from audio;
select * from system_info;
SELECT * FROM keystrokes;

truncate table screenshot;
truncate table audio;
truncate table system_info;
truncate table keystrokes;
truncate table video;
DESCRIBE screenshot;
DESCRIBE audio;
DESCRIBE keystrokes;
ALTER TABLE screenshot ADD COLUMN Filename VARCHAR(255);
ALTER TABLE audio ADD COLUMN Filename VARCHAR(255);