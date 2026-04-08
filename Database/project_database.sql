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
-- Seed Data (One Piece Themed)
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
-- OFFICERS (Marines)
-- ============================================================

INSERT INTO Officer (name, rank, badge_number, team_id) VALUES
('Sengoku',             'Detective',    'B1001', 1),
('Monkey D. Garp',      'Sergeant',     'B1002', 2),
('Aokiji',              'Officer',      'B1003', 3),
('Sakazuki',            'Detective',    'B1004', 1),
('Borsalino',           'Lieutenant',   'B1005', 2),
('Smoker',              'Officer',      'B1006', 4),
('Issho',               'Sergeant',     'B1007', 5),
('Coby',                'Detective',    'B1008', 3),
('Tashigi',             'Officer',      'B1009', 4),
('Tsuru',               'Lieutenant',   'B1010', 1);

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
-- CRIMINALS (Pirates — 51 total)
-- ============================================================

INSERT INTO Criminal (name, age, date_of_birth, gender, physical_description, is_repeat_offender) VALUES
('Edward "Whitebeard" Newgate',     72, '1951-04-06', 'Male',   'Enormous build, white mustache, bisento scar across chest',                   TRUE),
('Kaido of the Beasts',              59, '1964-05-01', 'Male',   'Massive frame, spiked club, dragon tattoo covering left arm',                 TRUE),
('Charlotte "Big Mom" Linlin',       68, '1955-02-15', 'Female', 'Enormous build, pink hair, homura earrings, candy cane weapon',                TRUE),
('Red-Haired Shanks',                39, '1984-03-09', 'Male',   'Red hair, missing left arm, three scar marks over left eye',                  TRUE),
('Marshall D. "Blackbeard" Teach',   40, '1983-08-22', 'Male',   'Large build, black beard, multiple missing teeth, dual pistols',              TRUE),
('Marco the Phoenix',                43, '1980-10-05', 'Male',   'Blonde hair, blue flames, phoenix tattoo on back',                            TRUE),
('Portgas D. Ace',                   20, '2003-01-01', 'Male',   'Freckles, fire tattoo on back reading "ASCE", cowboy hat',                    TRUE),
('Vista',                            47, '1976-07-14', 'Male',   'Flower-shaped hat, dual swords, handlebar mustache',                          FALSE),
('Queen the Plague',                 56, '1967-09-09', 'Male',   'Long hair in bun, cyborg arm, mammoth transformation marks',                  TRUE),
('King the Wildfire',                47, '1976-03-28', 'Male',   'All-black mask and wings, extremely tall, lunarian tribal marks',             TRUE),
('Jack the Drought',                 35, '1988-07-03', 'Male',   'Pale skin, large tusks, metal jaw implant, blonde braid',                     TRUE),
('Ulti',                             22, '2001-11-18', 'Female', 'Horned headgear, short blue hair, dinosaur scale tattoo on neck',              FALSE),
('Charlotte Katakuri',               48, '1975-05-10', 'Male',   'Scarred mouth hidden by scarf, tallest of siblings, mochi body',               TRUE),
('Charlotte Cracker',                45, '1978-01-28', 'Male',   'Biscuit-armor exterior, thin frame underneath, rapier sword',                TRUE),
('Charlotte Smoothie',               35, '1988-09-28', 'Female', 'Half-giant build, braided green hair, twin swords',                             FALSE),
('Charlotte Perospero',              50, '1973-03-11', 'Male',   'Candy-cane staff, lollipop in mouth, tall lanky frame',                       FALSE),
('Shiryu of the Rain',               41, '1982-05-30', 'Male',   'Rain coat, long sword, glasses, emotionless expression',                       TRUE),
('Van Augur the Supersonic',         28, '1995-08-10', 'Male',   'Long black cloak, sniper rifle, skeletal face paint',                          TRUE),
('Laffitte',                         34, '1989-12-04', 'Male',   'Top hat, white suit, bird wings on back, walking cane',                        FALSE),
('Monkey D. Luffy',                  19, '2004-05-05', 'Male',   'Straw hat, red vest, scar under left eye, rubber-like agility',               TRUE),
('Roronoa Zoro',                     21, '2002-11-11', 'Male',   'Green hair, three earrings left ear, three swords, scar over left eye',       TRUE),
('Trafalgar D. Water Law',           26, '1997-10-06', 'Male',   'Spotted hat, tattoos covering hands and neck, nodachi sword',                 TRUE),
('Eustass "Captain" Kid',            23, '2000-01-10', 'Male',   'Red hair, goggles, mechanical left arm, massive build',                       TRUE),
('Killer',                           23, '2000-02-02', 'Male',   'White mask, blonde hair, dual scythe blades on wrists',                       TRUE),
('Basil Hawkins',                    29, '1994-09-09', 'Male',   'Long blonde hair, voodoo straw doll, tarot card motifs',                      FALSE),
('Scratchmen Apoo',                  29, '1994-03-19', 'Male',   'Dreadlocks, musical instrument body, skeletal face paint',                     FALSE),
('Urouge the Mad Monk',              47, '1976-01-21', 'Male',   'Wings on back, large monk staff, heavyset build, monk robes',                 FALSE),
('X Drake',                          33, '1990-10-24', 'Male',   'Tall, military coat, anchor saber, dinosaur transformation marks',            FALSE),
('Dracule "Hawkeye" Mihawk',         43, '1980-03-09', 'Male',   'Hawk-like yellow eyes, black cape, cross-shaped necklace, black blade Yoru',   TRUE),
('Sir Crocodile',                    46, '1977-09-05', 'Male',   'Hook for right hand, scarred face, long coat, cigar always lit',               TRUE),
('Donquixote Doflamingo',            41, '1982-10-23', 'Male',   'Feathered pink coat, sunglasses, long blonde hair, string tattoos',           TRUE),
('Boa Hancock',                      31, '1992-09-02', 'Female', 'Extremely tall, black hair to waist, snake earrings, Gorgon symbol on back',   FALSE),
('Bartholomew Kuma',                 47, '1976-12-09', 'Male',   'Massive cyborg frame, Bible always in hand, paw-print symbol on palms',       TRUE),
('Gecko Moria',                      50, '1973-09-06', 'Male',   'Pale skin, stitched face, enormous pale cross-shaped tattoo, zombie hordes',  TRUE),
('Jinbe',                            46, '1977-04-02', 'Male',   'Whale shark fishman, blue skin, large build, traditional fishman karate robes', FALSE),
('Silvers Rayleigh',                 78, '1945-05-13', 'Male',   'Silver hair, round glasses, scar over right eye, old but powerful build',      TRUE),
('Scopper Gaban',                    54, '1969-07-07', 'Male',   'Axe weapons, scruffy hair, tattoos on both arms',                              FALSE),
('Nami',                             20, '2003-07-03', 'Female', 'Orange hair, tattoo of pinwheel and mikan on left shoulder, climate baton',       TRUE),
('Nico Robin',                       28, '1995-02-06', 'Female', 'Black hair, blue eyes, "Poneglyphs" tattoos on arms, devil fruit ability',      TRUE),
('Usopp',                            19, '2004-04-01', 'Male',   'Long nose, curly black hair, goggles, slingshot weapon',                      FALSE),
('Vinsmoke Sanji',                   21, '2002-03-02', 'Male',   'Blonde hair covering right eye, black suit, curly eyebrow, leg-based fighter', TRUE),
('Charlotte Pudding',                16, '2010-06-25', 'Female', 'Brown wavy hair, third eye on forehead covered by bangs, candy bullets',       FALSE),
('Yamato',                           28, '1995-11-03', 'Female', 'Long white hair, oni horns, traditional Japanese robes, kanabo club',          FALSE),
('Carrot',                           21, '2002-05-24', 'Female', 'White rabbit ears, orange eyes, bunny features, electro ability',              FALSE),
('Nefertari Vivi',                   18, '2006-02-02', 'Female', 'Blue hair, princess attire, Alabasta royal symbol tattoo',                       FALSE),
('Buggy the Clown',                  39, '1984-08-08', 'Male',   'Red nose, blue hair divided by line, clown makeup, detachable body parts',    TRUE),
('Miss All Sunday',                  26, '1998-02-06', 'Female', 'Green hair, sunglasses, long coat, alias used while with Baroque Works',       FALSE),
('Arlong',                           41, '1982-05-03', 'Male',   'Sawshark fishman, blue skin, massive serrated nose, fishman karate',          TRUE),
('Caesar Clown',                     46, '1977-04-09', 'Male',   'Mad scientist appearance, large head, gas mask, lab coat stained with chemicals', TRUE),
('Vergo',                            41, '1982-10-06', 'Male',   'Tall, business attire, bamboo staff, food always stuck to face',               TRUE),
('Monet',                            25, '1998-01-01', 'Female', 'Harpy wings, snow-white feathers, glasses, Doflamingo tattoo on wrist',          FALSE),
('Trebol',                           52, '1971-03-18', 'Male',   'Disgusting mucus-covered body, long cloak, stick weapon, sticky substance trail', TRUE);

-- ============================================================
-- CRIMES (60 total)
-- ============================================================

INSERT INTO Crime (description, method_used, location, city, latitude, longitude, date_time, status) VALUES
('Armed robbery at convenience store',                'Armed Robbery',     '5th Ave & 23rd St',            'New York',      40.7448,  -73.9894,  '2024-01-05 21:30:00', 'Open'),
('Residential break-in and theft',                    'Forced Entry',      '88 Maple Drive',               'Chicago',       41.8340,  -87.7320,  '2024-01-08 03:15:00', 'Open'),
('Drug deal bust near park',                          'Drug Distribution', 'Central Park North',           'New York',      40.7994,  -73.9530,  '2024-01-09 18:00:00', 'Closed'),
('Carjacking at red light',                           'Armed Robbery',     'Highway 90 Exit 14',           'Houston',       29.7630,  -95.3632,  '2024-01-11 22:45:00', 'Open'),
('Online fraud and identity theft',                   'Phishing Scam',     'Remote/Online',                'Los Angeles',   34.0522, -118.2437,  '2024-01-13 10:00:00', 'Open'),
('Assault with weapon outside nightclub',             'Armed Assault',     '12 Club Row',                  'Miami',         25.7617,  -80.1918,  '2024-01-15 01:00:00', 'Closed'),
('Warehouse robbery using forced entry',              'Forced Entry',      '300 Industrial Blvd',          'Chicago',       41.8100,  -87.7200,  '2024-01-17 02:30:00', 'Open'),
('Drug trafficking intercept at airport',             'Drug Distribution', 'JFK Airport Terminal 4',       'New York',      40.6413,  -73.7781,  '2024-01-19 14:00:00', 'Open'),
('Phishing ring targeting elderly citizens',          'Phishing Scam',     'Multiple Locations',           'Phoenix',       33.4484, -112.0740,  '2024-01-21 09:00:00', 'Open'),
('Bank robbery using armed threat',                   'Armed Robbery',     'First National Bank',          'Dallas',        32.7767,  -96.7970,  '2024-01-23 11:15:00', 'Open'),
('Jewelry store smash-and-grab',                      'Armed Robbery',     '14 Diamond Row',               'New York',      40.7580,  -73.9855,  '2024-01-25 14:20:00', 'Open'),
('Chemical weapon formula theft from lab',            'Burglary',          'BioSynth Research Center',     'Boston',        42.3601,  -71.0589,  '2024-01-26 02:00:00', 'Open'),
('Mass narcotics distribution at concert',            'Drug Distribution', 'Arena District',               'Los Angeles',   34.0430, -118.2673,  '2024-01-27 22:00:00', 'Closed'),
('Armored truck hijacking on highway',                'Armed Robbery',     'I-95 Mile Marker 42',          'Philadelphia',  39.9526,  -75.1652,  '2024-01-28 08:30:00', 'Open'),
('Credit card skimming network bust',                 'Phishing Scam',     'Multiple ATMs citywide',       'Las Vegas',     36.1699, -115.1398,  '2024-01-29 11:00:00', 'Closed'),
('Assassination attempt on business executive',       'Armed Assault',     'Grand Hotel Lobby',            'Chicago',       41.8858,  -87.6181,  '2024-01-30 19:45:00', 'Open'),
('Illegal weapons cache discovered at docks',         'Arms Trafficking',  'Pier 17 Warehouse',            'New York',      40.7063,  -74.0010,  '2024-01-31 06:00:00', 'Open'),
('Ransom kidnapping of shipping magnate',             'Kidnapping',        'Harbor District',              'Seattle',       47.6062, -122.3321,  '2024-02-01 20:00:00', 'Open'),
('Arson at rival gang headquarters',                  'Arson',             '55 West End Blvd',             'Detroit',       42.3314,  -83.0458,  '2024-02-02 03:30:00', 'Closed'),
('Cryptocurrency exchange hack',                      'Cybercrime',        'Remote/Online',                'San Francisco', 37.7749, -122.4194,  '2024-02-03 09:00:00', 'Open'),
('Hostage situation at pawn shop',                    'Armed Assault',     '202 Broad Street',             'Atlanta',       33.7490,  -84.3880,  '2024-02-04 16:00:00', 'Closed'),
('Illegal gambling den raided',                       'Organized Crime',   'Basement of Lucky Dragon',     'New York',      40.7282,  -73.7949,  '2024-02-05 23:00:00', 'Closed'),
('Street-level heroin distribution bust',             'Drug Distribution', 'East 5th & Vernon Ave',        'Chicago',       41.7943,  -87.6022,  '2024-02-06 17:30:00', 'Open'),
('Cargo ship looting at port',                        'Forced Entry',      'Port of Houston Dock 9',       'Houston',       29.7275,  -95.2680,  '2024-02-07 01:00:00', 'Open'),
('Corporate espionage and data breach',               'Cybercrime',        'TechCorp HQ',                  'San Jose',      37.3382, -121.8863,  '2024-02-08 12:00:00', 'Open'),
('Museum heist stolen ancient artifacts',             'Burglary',          'City History Museum',          'Boston',        42.3555,  -71.0655,  '2024-02-09 02:30:00', 'Open'),
('Drive-by shooting outside restaurant',              'Armed Assault',     '88 Harbor Lights Drive',       'Miami',         25.7743,  -80.1937,  '2024-02-10 21:00:00', 'Closed'),
('Fentanyl lab discovered in suburb',                 'Drug Distribution', '14 Willow Creek Court',        'Phoenix',       33.4255, -112.0685,  '2024-02-11 10:00:00', 'Open'),
('Extortion of local restaurant owners',              'Organized Crime',   'Chinatown Business District',  'San Francisco', 37.7941, -122.4078,  '2024-02-12 14:00:00', 'Open'),
('Fake ID and passport forgery ring',                 'Forgery',           'Underground Print Shop',       'New York',      40.7127,  -74.0059,  '2024-02-13 09:30:00', 'Closed'),
('Human trafficking network intercepted',             'Kidnapping',        'Warehouse near train yard',    'Dallas',        32.7814,  -96.8207,  '2024-02-14 04:00:00', 'Open'),
('Bank account hacking spree',                        'Cybercrime',        'Remote/Online',                'Miami',         25.7617,  -80.1918,  '2024-02-15 08:00:00', 'Open'),
('Mob-ordered building demolition sabotage',          'Arson',             '300 Grand Pier Blvd',          'Chicago',       41.8955,  -87.6269,  '2024-02-16 03:00:00', 'Closed'),
('Smuggling of exotic weapons via shipping container','Arms Trafficking',  'Port of Los Angeles Dock 5',   'Los Angeles',   33.7282, -118.2620,  '2024-02-17 05:30:00', 'Open'),
('Riot incitement and looting spree',                 'Organized Crime',   'Downtown Shopping District',   'Portland',      45.5051, -122.6750,  '2024-02-18 18:00:00', 'Closed'),
('Child endangerment via drugged candy distribution', 'Drug Distribution', 'Rosemont Elementary Area',     'Houston',       29.8174,  -95.4048,  '2024-02-19 15:00:00', 'Open'),
('Blackmail of city council members',                 'Organized Crime',   'City Hall District',           'New York',      40.7128,  -74.0060,  '2024-02-20 10:00:00', 'Open'),
('Luxury car theft ring bust',                        'Theft',             'Prestige Auto Dealer Row',     'Las Vegas',     36.0953, -115.1745,  '2024-02-21 22:00:00', 'Closed'),
('Illegal firearm modifications shop raided',         'Arms Trafficking',  '77 Backstreet Alley',          'Detroit',       42.3534,  -83.0654,  '2024-02-22 13:00:00', 'Open'),
('Night club drugging and robbery',                   'Armed Robbery',     'Club Neon 9th Street',         'Las Vegas',     36.1716, -115.1391,  '2024-02-23 02:30:00', 'Open'),
('Cyber attack on power grid',                        'Cybercrime',        'Remote/Online',                'Washington DC', 38.9072,  -77.0369,  '2024-02-24 07:00:00', 'Open'),
('Illegal animal trafficking at auction house',       'Organized Crime',   'Southside Auction House',      'Atlanta',       33.7350,  -84.4240,  '2024-02-25 16:00:00', 'Closed'),
('Protection money shakedown of food vendors',        'Organized Crime',   'Waterfront Market',            'Seattle',       47.6089, -122.3407,  '2024-02-26 11:00:00', 'Open'),
('Rooftop sniper attack on police convoy',            'Armed Assault',     'Midtown Expressway Bridge',    'New York',      40.7549,  -73.9840,  '2024-02-27 14:30:00', 'Open'),
('Meth lab explosion and bust',                       'Drug Distribution', '19 Industrial Park Lane',      'Albuquerque',   35.0853, -106.6056,  '2024-02-28 06:00:00', 'Closed'),
('Identity fraud using stolen hospital records',      'Phishing Scam',     'MedCore Hospital',             'Boston',        42.3380,  -71.1068,  '2024-02-29 09:00:00', 'Open'),
('Armed takeover of luxury apartment complex',        'Armed Robbery',     'Pinnacle Tower Floor 30',      'Chicago',       41.8999,  -87.6246,  '2024-03-01 23:00:00', 'Open'),
('Bomb threat at government building',                'Armed Assault',     'Federal Plaza',                'San Francisco', 37.7802, -122.4194,  '2024-03-02 10:00:00', 'Closed'),
('Underground fight club operation exposed',          'Organized Crime',   'Abandoned Factory District',   'Detroit',       42.3673,  -83.0733,  '2024-03-03 20:00:00', 'Closed'),
('Safe cracking at luxury hotel vault',               'Burglary',          'Grand Meridian Hotel',         'New York',      40.7614,  -73.9776,  '2024-03-04 04:00:00', 'Open'),
('Poison gas release in subway station',              'Armed Assault',     'Union Square Station',         'New York',      40.7359,  -73.9911,  '2024-03-05 08:30:00', 'Open'),
('Street gang territorial murder',                    'Armed Assault',     'Southside Park',               'Chicago',       41.7945,  -87.5947,  '2024-03-06 01:00:00', 'Closed'),
('Money laundering through restaurant chain',           'Organized Crime',   'Multiple Locations',           'Miami',         25.7617,  -80.1918,  '2024-03-07 10:00:00', 'Open'),
('Drone-assisted drug drop in prison yard',           'Drug Distribution', 'Westgate Correctional',        'Phoenix',       33.4784, -112.0748,  '2024-03-08 14:00:00', 'Open'),
('Ransomware attack on hospital network',             'Cybercrime',        'Metro General Hospital',       'Houston',       29.7541,  -95.3677,  '2024-03-09 06:00:00', 'Open'),
('Forged artwork sold through gallery',               'Forgery',           'Prestige Art Gallery',         'Los Angeles',   34.0440, -118.2440,  '2024-03-10 15:00:00', 'Closed'),
('Organized shoplifting crew targeting malls',        'Theft',             'Westfield Mall',               'San Jose',      37.3250, -121.9300,  '2024-03-11 13:00:00', 'Closed'),
('Kidnapping for organ trafficking',                 'Kidnapping',        'Harbor Side Clinic',           'Houston',       29.7523,  -95.3853,  '2024-03-12 03:00:00', 'Open'),
('Hacking of election database',                     'Cybercrime',        'Remote/Online',                'Washington DC', 38.9072,  -77.0369,  '2024-03-13 11:00:00', 'Open'),
('Large-scale cocaine seizure at warehouse',          'Drug Distribution', '500 Portside Ave',             'Miami',         25.7748,  -80.1985,  '2024-03-14 05:00:00', 'Open');

-- ============================================================
-- CRIME INVOLVEMENT (53 records)
-- ============================================================

INSERT INTO CrimeInvolvement (criminal_id, crime_id) VALUES
(2, 1), (2, 4), (2, 10), (2, 14), (2, 47),
(5, 2), (5, 7), (5, 17), (5, 34),
(31, 5), (31, 9), (31, 22), (31, 37), (31, 53),
(30, 3), (30, 8), (30, 23), (30, 60),
(49, 5), (49, 12), (49, 28), (49, 45),
(10, 6), (10, 4), (10, 16),
(1, 10), (1, 47),
(48, 7), (48, 24),
(3, 18), (3, 31),
(52, 29), (52, 43),
(20, 11), (20, 38),
(21, 6), (21, 44),
(22, 20), (22, 55),
(23, 14), (23, 34),
(11, 35), (11, 51),
(13, 40), (13, 52),
(29, 44), (29, 50),
(46, 30), (46, 56),
(39, 25), (39, 59),
(17, 16), (17, 52);

-- ============================================================
-- WARRANTS (15 total)
-- ============================================================

INSERT INTO Warrant (criminal_id, issue_date, status) VALUES
(2, '2024-01-06', 'Active'),
(5, '2024-01-09', 'Active'),
(30, '2024-01-10', 'Active'),
(10, '2024-01-16', 'Active'),
(31, '2023-11-01', 'Cancelled'),
(1, '2024-01-24', 'Active'),
(48, '2023-09-15', 'Cancelled'),
(13, '2024-01-20', 'Active'),
(49, '2024-01-22', 'Active'),
(20, '2024-01-15', 'Active'),
(3, '2024-02-02', 'Active'),
(11, '2024-03-06', 'Active'),
(52, '2024-02-13', 'Active'),
(29, '2024-02-28', 'Active'),
(23, '2024-01-29', 'Active');

-- ============================================================
-- CASE RECORDS (60 total)
-- ============================================================

INSERT INTO CaseRecord (crime_id, status, opened_date) VALUES
(1, 'Open', '2024-01-05'), (2, 'Open', '2024-01-08'), (3, 'Finished', '2024-01-09'), (4, 'Open', '2024-01-11'), (5, 'Open', '2024-01-13'),
(6, 'Finished', '2024-01-15'), (7, 'Open', '2024-01-17'), (8, 'Open', '2024-01-19'), (9, 'Open', '2024-01-21'), (10, 'Open', '2024-01-23'),
(11, 'Open', '2024-01-25'), (12, 'Open', '2024-01-26'), (13, 'Finished', '2024-01-27'), (14, 'Open', '2024-01-28'), (15, 'Finished', '2024-01-29'),
(16, 'Open', '2024-01-30'), (17, 'Open', '2024-01-31'), (18, 'Open', '2024-02-01'), (19, 'Finished', '2024-02-02'), (20, 'Open', '2024-02-03'),
(21, 'Finished', '2024-02-04'), (22, 'Finished', '2024-02-05'), (23, 'Open', '2024-02-06'), (24, 'Open', '2024-02-07'), (25, 'Open', '2024-02-08'),
(26, 'Open', '2024-02-09'), (27, 'Finished', '2024-02-10'), (28, 'Open', '2024-02-11'), (29, 'Open', '2024-02-12'), (30, 'Finished', '2024-02-13'),
(31, 'Open', '2024-02-14'), (32, 'Open', '2024-02-15'), (33, 'Finished', '2024-02-16'), (34, 'Open', '2024-02-17'), (35, 'Finished', '2024-02-18'),
(36, 'Open', '2024-02-19'), (37, 'Open', '2024-02-20'), (38, 'Finished', '2024-02-21'), (39, 'Open', '2024-02-22'), (40, 'Open', '2024-02-23'),
(41, 'Open', '2024-02-24'), (42, 'Finished', '2024-02-25'), (43, 'Open', '2024-02-26'), (44, 'Open', '2024-02-27'), (45, 'Finished', '2024-02-28'),
(46, 'Open', '2024-02-29'), (47, 'Open', '2024-03-01'), (48, 'Finished', '2024-03-02'), (49, 'Finished', '2024-03-03'), (50, 'Open', '2024-03-04'),
(51, 'Open', '2024-03-05'), (52, 'Finished', '2024-03-06'), (53, 'Open', '2024-03-07'), (54, 'Open', '2024-03-08'), (55, 'Open', '2024-03-09'),
(56, 'Finished', '2024-03-10'), (57, 'Finished', '2024-03-11'), (58, 'Open', '2024-03-12'), (59, 'Open', '2024-03-13'), (60, 'Open', '2024-03-14');

-- ============================================================
-- UPDATE REPEAT OFFENDER FLAG
-- ============================================================

UPDATE Criminal c
JOIN (
    SELECT criminal_id, COUNT(*) AS crime_count
    FROM CrimeInvolvement
    GROUP BY criminal_id
) ci ON c.criminal_id = ci.criminal_id
SET c.is_repeat_offender = CASE WHEN ci.crime_count >= 3 THEN TRUE ELSE FALSE END;
