-- ============================================================
-- CAIS: Criminal Analysis & Investigation System
-- Database Schema
-- Course: CSE370 | MySQL
-- ============================================================

-- ============================================================
-- 1. ADMIN AUTH
-- ============================================================

CREATE TABLE Admin (
    admin_id        INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    role            VARCHAR(30) DEFAULT 'admin',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 2. OFFICERS & TEAMS
-- ============================================================

CREATE TABLE Team (
    team_id     INT AUTO_INCREMENT PRIMARY KEY,
    team_name   VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Officer (
    officer_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    rank            VARCHAR(50) NOT NULL,
    badge_number    VARCHAR(30) NOT NULL UNIQUE,
    team_id         INT,
    FOREIGN KEY (team_id) REFERENCES Team(team_id)
        ON DELETE SET NULL
);

CREATE TABLE Shift (
    shift_id    INT AUTO_INCREMENT PRIMARY KEY,
    officer_id  INT NOT NULL,
    date_worked DATE NOT NULL,
    hours       DECIMAL(4,2),
    FOREIGN KEY (officer_id) REFERENCES Officer(officer_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 3. CRIMINALS
-- ============================================================

CREATE TABLE Criminal (
    criminal_id             INT AUTO_INCREMENT PRIMARY KEY,
    name                    VARCHAR(100) NOT NULL,
    age                     INT,
    date_of_birth           DATE,
    gender                  ENUM('Male', 'Female', 'Other'),
    physical_description    TEXT,
    is_repeat_offender      BOOLEAN DEFAULT FALSE
);

CREATE TABLE Nickname (
    nickname_id     INT AUTO_INCREMENT PRIMARY KEY,
    criminal_id     INT NOT NULL,
    alias           VARCHAR(100) NOT NULL,
    FOREIGN KEY (criminal_id) REFERENCES Criminal(criminal_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 4. VICTIMS
-- ============================================================

CREATE TABLE Victim (
    victim_id   INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL
);

CREATE TABLE Victim_Phone (
    phone_id    INT AUTO_INCREMENT PRIMARY KEY,
    victim_id   INT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (victim_id) REFERENCES Victim(victim_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 5. CRIMES
-- ============================================================

CREATE TABLE Crime (
    crime_id        INT AUTO_INCREMENT PRIMARY KEY,
    description     TEXT NOT NULL,
    method_used     VARCHAR(150),
    location        VARCHAR(200),
    city            VARCHAR(100),
    latitude        DECIMAL(9,6),
    longitude       DECIMAL(9,6),
    date_time       DATETIME,
    status          ENUM('Open', 'Closed') DEFAULT 'Open'
);

CREATE TABLE Evidence (
    evidence_id     INT AUTO_INCREMENT PRIMARY KEY,
    crime_id        INT NOT NULL,
    type            VARCHAR(100) NOT NULL,
    description     TEXT,
    FOREIGN KEY (crime_id) REFERENCES Crime(crime_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 6. BRIDGE TABLES (M:N Relationships)
-- ============================================================

-- Officer <-> Crime (with date worked)
CREATE TABLE Investigates (
    officer_id  INT NOT NULL,
    crime_id    INT NOT NULL,
    date_worked DATE,
    PRIMARY KEY (officer_id, crime_id),
    FOREIGN KEY (officer_id) REFERENCES Officer(officer_id)
        ON DELETE CASCADE,
    FOREIGN KEY (crime_id) REFERENCES Crime(crime_id)
        ON DELETE CASCADE
);

-- Criminal <-> Crime
CREATE TABLE CrimeInvolvement (
    criminal_id INT NOT NULL,
    crime_id    INT NOT NULL,
    PRIMARY KEY (criminal_id, crime_id),
    FOREIGN KEY (criminal_id) REFERENCES Criminal(criminal_id)
        ON DELETE CASCADE,
    FOREIGN KEY (crime_id) REFERENCES Crime(crime_id)
        ON DELETE CASCADE
);

-- Victim <-> Crime
CREATE TABLE CrimeVictim (
    victim_id   INT NOT NULL,
    crime_id    INT NOT NULL,
    PRIMARY KEY (victim_id, crime_id),
    FOREIGN KEY (victim_id) REFERENCES Victim(victim_id)
        ON DELETE CASCADE,
    FOREIGN KEY (crime_id) REFERENCES Crime(crime_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 7. WARRANTS
-- ============================================================

CREATE TABLE Warrant (
    warrant_id      INT AUTO_INCREMENT PRIMARY KEY,
    criminal_id     INT NOT NULL,
    issue_date      DATE NOT NULL,
    status          ENUM('Active', 'Cancelled') DEFAULT 'Active',
    FOREIGN KEY (criminal_id) REFERENCES Criminal(criminal_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 8. INTERROGATION
-- ============================================================

CREATE TABLE Interrogation (
    interrogation_id    INT AUTO_INCREMENT PRIMARY KEY,
    officer_id          INT NOT NULL,
    criminal_id         INT NOT NULL,
    date                DATETIME NOT NULL,
    notes               TEXT,
    FOREIGN KEY (officer_id) REFERENCES Officer(officer_id)
        ON DELETE CASCADE,
    FOREIGN KEY (criminal_id) REFERENCES Criminal(criminal_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 9. CASES
-- ============================================================

CREATE TABLE CaseRecord (
    case_id     INT AUTO_INCREMENT PRIMARY KEY,
    crime_id    INT NOT NULL UNIQUE,
    status      ENUM('Open', 'Finished') DEFAULT 'Open',
    opened_date DATE,
    FOREIGN KEY (crime_id) REFERENCES Crime(crime_id)
        ON DELETE CASCADE
);

-- ============================================================
-- 10. COURT
-- ============================================================

CREATE TABLE Court (
    court_id    INT AUTO_INCREMENT PRIMARY KEY,
    case_id     INT NOT NULL,
    court_date  DATE NOT NULL,
    judge_name  VARCHAR(100),
    FOREIGN KEY (case_id) REFERENCES CaseRecord(case_id)
        ON DELETE CASCADE
);

-- ============================================================
-- INDEXES (for fast search - Feature 5, CO3)
-- ============================================================

CREATE INDEX idx_officer_rank    ON Officer(rank);
CREATE INDEX idx_officer_team    ON Officer(team_id);
CREATE INDEX idx_crime_method    ON Crime(method_used);
CREATE INDEX idx_warrant_status  ON Warrant(status);
CREATE INDEX idx_case_status     ON CaseRecord(status);

-- ============================================================
-- VIEWS
-- ============================================================

-- Feature 11: BOLO List
CREATE VIEW BOLO_List AS
SELECT
    w.warrant_id,
    c.criminal_id,
    c.name AS criminal_name,
    c.age,
    c.physical_description,
    w.issue_date
FROM Warrant w
JOIN Criminal c ON w.criminal_id = c.criminal_id
WHERE w.status = 'Active';

-- Feature 2: Repeat Offender Alert
CREATE VIEW Repeat_Offenders AS
SELECT
    c.criminal_id,
    c.name,
    c.age,
    COUNT(ci.crime_id) AS total_crimes,
    CASE
        WHEN COUNT(ci.crime_id) >= 3 THEN TRUE
        ELSE FALSE
    END AS is_repeat_offender
FROM Criminal c
LEFT JOIN CrimeInvolvement ci ON c.criminal_id = ci.criminal_id
GROUP BY c.criminal_id, c.name, c.age
ORDER BY total_crimes DESC;

-- Feature 1: Crime Pattern Finder
CREATE VIEW Crime_Patterns AS
SELECT
    method_used,
    COUNT(*) AS total_crimes,
    GROUP_CONCAT(crime_id ORDER BY date_time SEPARATOR ', ') AS crime_ids
FROM Crime
WHERE method_used IS NOT NULL
GROUP BY method_used
ORDER BY total_crimes DESC;

-- ============================================================
-- Seed Data (Fake Data for Testing)
-- ============================================================

-- ============================================================
-- ADMIN
-- ============================================================

INSERT INTO Admin (username, password_hash, role) VALUES
('admin',       'pbkdf2_sha256$admin123',   'admin'),
('superuser',   'pbkdf2_sha256$super456',   'superadmin');

-- ============================================================
-- TEAMS
-- ============================================================

INSERT INTO Team (team_name) VALUES
('Homicide'),
('Narcotics'),
('Cybercrime'),
('Traffic'),
('Robbery');

-- ============================================================
-- OFFICERS
-- ============================================================

INSERT INTO Officer (name, rank, badge_number, team_id) VALUES
('James Carter',    'Detective',    'B1001', 1),
('Maria Lopez',     'Sergeant',     'B1002', 2),
('David Kim',       'Officer',      'B1003', 3),
('Sarah Thompson',  'Detective',    'B1004', 1),
('Robert Hayes',    'Lieutenant',   'B1005', 2),
('Emily Nguyen',    'Officer',      'B1006', 4),
('Marcus Brown',    'Sergeant',     'B1007', 5),
('Linda Patel',     'Detective',    'B1008', 3),
('Chris Walker',    'Officer',      'B1009', 4),
('Angela Foster',   'Lieutenant',   'B1010', 1);

-- ============================================================
-- SHIFTS
-- ============================================================

INSERT INTO Shift (officer_id, date_worked, hours) VALUES
(1, '2024-01-10', 8.0),
(1, '2024-01-11', 8.0),
(2, '2024-01-10', 8.0),
(3, '2024-01-12', 8.0),
(4, '2024-01-13', 8.0),
(5, '2024-01-14', 8.0),
(6, '2024-01-10', 8.0),
(7, '2024-01-11', 8.0),
(8, '2024-01-15', 8.0),
(9, '2024-01-16', 8.0);

-- ============================================================
-- CRIMINALS
-- ============================================================

INSERT INTO Criminal (name, age, date_of_birth, gender, physical_description, is_repeat_offender) VALUES
('Tony Deluca',         34, '1990-03-15', 'Male',   'Scar on left cheek, snake tattoo on neck',         TRUE),
('Marcus "Ghost" Reed', 29, '1995-07-22', 'Male',   'Teardrop tattoo under right eye, bald',            TRUE),
('Elena Voss',          41, '1983-11-05', 'Female', 'Red hair, rose tattoo on left wrist',              FALSE),
('Jerome "J-Dog" Hill', 26, '1998-01-30', 'Male',   'Tall, thin build, cross tattoo on forearm',        TRUE),
('Sandra Wu',           38, '1986-09-14', 'Female', 'Short, glasses, no visible tattoos',               FALSE),
('Ray "Blade" Torres',  32, '1992-06-18', 'Male',   'Stocky build, barbed wire tattoo around bicep',    TRUE),
('Kevin Nash',          45, '1979-12-01', 'Male',   'Greying hair, scar on right hand',                 FALSE),
('Diane Mercer',        27, '1997-04-25', 'Female', 'Blue eyes, butterfly tattoo on shoulder',          FALSE);

-- ============================================================
-- NICKNAMES
-- ============================================================

INSERT INTO Nickname (criminal_id, alias) VALUES
(1, 'The Cobra'),
(1, 'Tony D'),
(2, 'Ghost'),
(2, 'The Shadow'),
(4, 'J-Dog'),
(4, 'Jerome the Fox'),
(6, 'Blade'),
(6, 'The Butcher');

-- ============================================================
-- VICTIMS
-- ============================================================

INSERT INTO Victim (name) VALUES
('Michael Scott'),
('Rachel Green'),
('Tom Hardy'),
('Lisa Monroe'),
('Carlos Rivera'),
('Nina Patel'),
('George Freeman'),
('Amy Chen');

-- ============================================================
-- VICTIM PHONES
-- ============================================================

INSERT INTO Victim_Phone (victim_id, phone_number) VALUES
(1, '555-101-2020'),
(1, '555-303-4040'),
(2, '555-202-3030'),
(3, '555-404-5050'),
(4, '555-505-6060'),
(5, '555-606-7070'),
(6, '555-707-8080'),
(7, '555-808-9090'),
(8, '555-909-1010');

-- ============================================================
-- CRIMES
-- ============================================================

INSERT INTO Crime (description, method_used, location, city, latitude, longitude, date_time, status) VALUES
('Armed robbery at convenience store',          'Armed Robbery',        '5th Ave & 23rd St',        'New York',     40.7448,  -73.9894,  '2024-01-05 21:30:00', 'Open'),
('Residential break-in and theft',              'Forced Entry',         '88 Maple Drive',           'Chicago',      41.8340,  -87.7320,  '2024-01-08 03:15:00', 'Open'),
('Drug deal bust near park',                    'Drug Distribution',    'Central Park North',       'New York',     40.7994,  -73.9530,  '2024-01-09 18:00:00', 'Closed'),
('Carjacking at red light',                     'Armed Robbery',        'Highway 90 Exit 14',       'Houston',      29.7630,  -95.3632,  '2024-01-11 22:45:00', 'Open'),
('Online fraud and identity theft',             'Phishing Scam',        'Remote/Online',            'Los Angeles',  34.0522, -118.2437,  '2024-01-13 10:00:00', 'Open'),
('Assault with weapon outside nightclub',       'Armed Assault',        '12 Club Row',              'Miami',        25.7617,  -80.1918,  '2024-01-15 01:00:00', 'Closed'),
('Warehouse robbery using forced entry',        'Forced Entry',         '300 Industrial Blvd',      'Chicago',      41.8100,  -87.7200,  '2024-01-17 02:30:00', 'Open'),
('Drug trafficking intercept at airport',       'Drug Distribution',    'JFK Airport Terminal 4',   'New York',     40.6413,  -73.7781,  '2024-01-19 14:00:00', 'Open'),
('Phishing ring targeting elderly citizens',    'Phishing Scam',        'Multiple Locations',       'Phoenix',      33.4484, -112.0740,  '2024-01-21 09:00:00', 'Open'),
('Bank robbery using armed threat',             'Armed Robbery',        'First National Bank',      'Dallas',       32.7767,  -96.7970,  '2024-01-23 11:15:00', 'Open');

-- ============================================================
-- EVIDENCE
-- ============================================================

INSERT INTO Evidence (crime_id, type, description) VALUES
(1, 'Firearm',      'Black 9mm handgun found near dumpster'),
(1, 'CCTV Footage', 'Store security camera footage of suspect'),
(2, 'Crowbar',      'Used to force open back window'),
(3, 'Narcotics',    '2kg of cocaine in sealed bags'),
(3, 'Mobile Phone', 'Burner phone with transaction records'),
(4, 'Firearm',      'Pistol recovered at scene'),
(5, 'Laptop',       'Laptop with phishing software installed'),
(6, 'Knife',        '6 inch blade with fingerprints'),
(7, 'Crowbar',      'Found at warehouse entrance'),
(8, 'Narcotics',    '5kg of heroin in checked luggage'),
(9, 'Laptop',       'Used to send phishing emails'),
(10, 'Firearm',     'Sawn-off shotgun left at scene');

-- ============================================================
-- INVESTIGATES (Officer <-> Crime)
-- ============================================================

INSERT INTO Investigates (officer_id, crime_id, date_worked) VALUES
(1, 1,  '2024-01-05'),
(4, 1,  '2024-01-06'),
(2, 3,  '2024-01-09'),
(5, 3,  '2024-01-10'),
(3, 5,  '2024-01-13'),
(8, 5,  '2024-01-14'),
(7, 4,  '2024-01-11'),
(1, 10, '2024-01-23'),
(4, 6,  '2024-01-15'),
(6, 4,  '2024-01-11');

-- ============================================================
-- CRIME INVOLVEMENT (Criminal <-> Crime)
-- ============================================================

INSERT INTO CrimeInvolvement (criminal_id, crime_id) VALUES
(1, 1),
(1, 4),
(1, 10),
(2, 2),
(2, 7),
(3, 5),
(3, 9),
(4, 3),
(4, 8),
(5, 5),
(6, 6),
(6, 4),
(7, 10),
(8, 9);

-- ============================================================
-- CRIME VICTIM
-- ============================================================

INSERT INTO CrimeVictim (victim_id, crime_id) VALUES
(1, 1),
(2, 2),
(3, 4),
(4, 6),
(5, 7),
(6, 9),
(7, 10),
(8, 5),
(1, 4),
(3, 10);

-- ============================================================
-- WARRANTS
-- ============================================================

INSERT INTO Warrant (criminal_id, issue_date, status) VALUES
(1, '2024-01-06', 'Active'),
(2, '2024-01-09', 'Active'),
(4, '2024-01-10', 'Active'),
(6, '2024-01-16', 'Active'),
(3, '2023-11-01', 'Cancelled'),
(7, '2024-01-24', 'Active'),
(5, '2023-09-15', 'Cancelled');

-- ============================================================
-- INTERROGATIONS
-- ============================================================

INSERT INTO Interrogation (officer_id, criminal_id, date, notes) VALUES
(1, 1,  '2024-01-07 10:00:00', 'Suspect denied involvement. Inconsistent alibi about location on night of robbery.'),
(4, 2,  '2024-01-10 14:00:00', 'Refused to answer questions. Lawyer present throughout.'),
(2, 4,  '2024-01-11 09:30:00', 'Admitted to being near the park but denied drug involvement.'),
(8, 3,  '2024-01-14 11:00:00', 'Cooperative. Provided names of two associates for further investigation.'),
(5, 6,  '2024-01-16 15:00:00', 'Aggressive behavior. Denied all charges. No useful information obtained.'),
(1, 7,  '2024-01-24 10:00:00', 'Claimed he was coerced. Willing to cooperate in exchange for reduced charges.');

-- ============================================================
-- CASES
-- ============================================================

INSERT INTO CaseRecord (crime_id, status, opened_date) VALUES
(1,  'Open',     '2024-01-05'),
(2,  'Open',     '2024-01-08'),
(3,  'Finished', '2024-01-09'),
(4,  'Open',     '2024-01-11'),
(5,  'Open',     '2024-01-13'),
(6,  'Finished', '2024-01-15'),
(7,  'Open',     '2024-01-17'),
(8,  'Open',     '2024-01-19'),
(9,  'Open',     '2024-01-21'),
(10, 'Open',     '2024-01-23');

-- ============================================================
-- COURT
-- ============================================================

INSERT INTO Court (case_id, court_date, judge_name) VALUES
(1,  '2024-02-10', 'Judge Patricia Moore'),
(2,  '2024-02-12', 'Judge Alan Grant'),
(3,  '2024-01-30', 'Judge Susan Lee'),
(3,  '2024-02-05', 'Judge Susan Lee'),
(4,  '2024-02-15', 'Judge Robert Hines'),
(5,  '2024-02-20', 'Judge Karen Watts'),
(6,  '2024-01-28', 'Judge David Park'),
(7,  '2024-02-18', 'Judge Alan Grant'),
(8,  '2024-02-25', 'Judge Patricia Moore'),
(10, '2024-03-01', 'Judge Robert Hines');

-- ============================================================
-- UPDATE REPEAT OFFENDER FLAG
-- (Run this after inserts or use the VIEW instead)
-- ============================================================

UPDATE Criminal c
JOIN (
    SELECT criminal_id, COUNT(*) AS crime_count
    FROM CrimeInvolvement
    GROUP BY criminal_id
) ci ON c.criminal_id = ci.criminal_id
SET c.is_repeat_offender = CASE WHEN ci.crime_count >= 3 THEN TRUE ELSE FALSE END;
