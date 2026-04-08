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
-- CRIMINALS (Pirates — 52 total)
-- ============================================================
-- Most dangerous flagged as repeat offenders:
-- Yonko, top commanders, notorious Warlords
-- ============================================================

INSERT INTO Criminal (name, age, date_of_birth, gender, physical_description, is_repeat_offender) VALUES
-- Yonko (4 most powerful pirates)
('Edward "Whitebeard" Newgate',     72, '1951-04-06', 'Male',   'Enormous build, white mustache, bisento scar across chest, strongest man alive',                                      TRUE),
('Kaido of the Beasts',              59, '1964-05-01', 'Male',   'Massive frame, spiked club, dragon tattoo covering left arm, indestructible body',                                     TRUE),
('Charlotte "Big Mom" Linlin',       68, '1955-02-15', 'Female', 'Enormous build, pink hair, homura earrings, candy cane weapon Prometheus and Napoleon',                                TRUE),
('Red-Haired Shanks',                39, '1984-03-09', 'Male',   'Red hair, missing left arm, three scar marks over left eye, conquerors haki user',                                     TRUE),
('Marshall D. "Blackbeard" Teach',   40, '1983-08-22', 'Male',   'Large build, black beard, multiple missing teeth, dual pistols, two devil fruit powers',                               TRUE),
-- Whitebeard Pirates commanders
('Marco the Phoenix',                43, '1980-10-05', 'Male',   'Blonde hair, blue flames, phoenix tattoo on back, first division commander',                                           TRUE),
('Portgas D. Ace',                   20, '2003-01-01', 'Male',   'Freckles, fire tattoo on back reading ASCE, cowboy hat, second division commander',                                    TRUE),
('Vista',                            47, '1976-07-14', 'Male',   'Flower-shaped hat, dual swords, handlebar mustache, fifth division commander',                                         FALSE),
('Jozu',                             45, '1978-06-20', 'Male',   'Diamond-encrusted skin, massive build, third division commander',                                                      FALSE),
-- Beast Pirates (Kaido crew)
('Queen the Plague',                 56, '1967-09-09', 'Male',   'Long hair in bun, cyborg arm, mammoth transformation marks, biological weapon specialist',                             TRUE),
('King the Wildfire',                47, '1976-03-28', 'Male',   'All-black mask and wings, extremely tall, lunarian tribal marks, only known lunarian survivor',                        TRUE),
('Jack the Drought',                 35, '1988-07-03', 'Male',   'Pale skin, large tusks, metal jaw implant, blonde braid, destroyed entire countries',                                  TRUE),
('Ulti',                             22, '2001-11-18', 'Female', 'Horned headgear, short blue hair, dinosaur scale tattoo on neck, flying-six member',                                   FALSE),
('Page One',                         20, '2003-09-22', 'Male',   'Spinosaurus features when transformed, spiked hair, flying-six member',                                                FALSE),
-- Big Mom Pirates commanders
('Charlotte Katakuri',               48, '1975-05-10', 'Male',   'Scarred mouth hidden by scarf, tallest of siblings, mochi body, never lost a battle before Luffy',                    TRUE),
('Charlotte Cracker',                45, '1978-01-28', 'Male',   'Biscuit-armor exterior, thin frame underneath, rapier sword, minister of biscuits',                                   TRUE),
('Charlotte Smoothie',               35, '1988-09-28', 'Female', 'Half-giant build, braided green hair, twin swords, wrings moisture from living beings',                                FALSE),
('Charlotte Perospero',              50, '1973-03-11', 'Male',   'Candy-cane staff, lollipop in mouth, tall lanky frame, eldest sibling of the Charlotte family',                        FALSE),
('Charlotte Oven',                   42, '1981-06-23', 'Male',   'Reddish skin, enormous build, heat-based abilities, minister of browned rice',                                         FALSE),
-- Blackbeard Pirates
('Shiryu of the Rain',               41, '1982-05-30', 'Male',   'Rain coat, long sword, glasses, emotionless expression, former impel down chief jailer',                              TRUE),
('Van Augur the Supersonic',         28, '1995-08-10', 'Male',   'Long black cloak, sniper rifle, skeletal face paint, never misses a target',                                           TRUE),
('Laffitte',                         34, '1989-12-04', 'Male',   'Top hat, white suit, bird wings on back, walking cane, former police officer turned pirate',                           FALSE),
('Doc Q',                            38, '1985-11-11', 'Male',   'Sickly pale complexion, rides skeletal horse, disease-based devil fruit, explosive apples',                            FALSE),
-- Worst Generation (11 Supernovas)
('Monkey D. Luffy',                  19, '2004-05-05', 'Male',   'Straw hat, red vest, scar under left eye, rubber-like agility, son of Revolutionary Dragon',                          TRUE),
('Roronoa Zoro',                     21, '2002-11-11', 'Male',   'Green hair, three earrings left ear, three swords including black blade, scar over left eye',                          TRUE),
('Trafalgar D. Water Law',           26, '1997-10-06', 'Male',   'Spotted hat, tattoos covering hands and neck, nodachi sword, room ability to rearrange matter',                        TRUE),
('Eustass "Captain" Kid',            23, '2000-01-10', 'Male',   'Red hair, goggles, mechanical prosthetic left arm, magnetic abilities, most bounty pre-timeskip',                      TRUE),
('Killer',                           23, '2000-02-02', 'Male',   'White mask, blonde hair, dual scythe blades on wrists, Kid pirates first mate',                                        TRUE),
('Basil Hawkins',                    29, '1994-09-09', 'Male',   'Long blonde hair, voodoo straw doll, tarot card motifs, transfers damage to others',                                   FALSE),
('Scratchmen Apoo',                  29, '1994-03-19', 'Male',   'Dreadlocks, musical instrument body, skeletal face paint, sound-based attacks',                                        FALSE),
('Urouge the Mad Monk',              47, '1976-01-21', 'Male',   'Wings on back, large monk staff, heavyset build, monk robes, grows stronger from damage',                              FALSE),
('X Drake',                          33, '1990-10-24', 'Male',   'Tall, military coat, anchor saber, dinosaur transformation, secret SWORD marine agent',                                FALSE),
('Capone "Gang" Bege',               38, '1985-01-24', 'Male',   'Short stature, three-piece suit, castle body, houses entire crew inside himself',                                      FALSE),
-- Former Warlords (Shichibukai)
('Dracule "Hawkeye" Mihawk',         43, '1980-03-09', 'Male',   'Hawk-like yellow eyes, black cape, cross-shaped necklace, black blade Yoru, greatest swordsman',                      TRUE),
('Sir Crocodile',                    46, '1977-09-05', 'Male',   'Hook for right hand, scarred face, long coat, cigar always lit, logia sand powers',                                    TRUE),
('Donquixote Doflamingo',            41, '1982-10-23', 'Male',   'Feathered pink coat, sunglasses, long blonde hair, string devil fruit, former world noble',                            TRUE),
('Boa Hancock',                      31, '1992-09-02', 'Female', 'Extremely tall, black hair to waist, snake earrings, Gorgon symbol on back, petrification ability',                   FALSE),
('Bartholomew Kuma',                 47, '1976-12-09', 'Male',   'Massive cyborg frame, Bible always in hand, paw-print symbol on palms, pacifista model',                              TRUE),
('Gecko Moria',                      50, '1973-09-06', 'Male',   'Pale skin, stitched face, enormous pale cross-shaped tattoo, controls army of zombies',                                TRUE),
('Jinbe',                            46, '1977-04-02', 'Male',   'Whale shark fishman, blue skin, large build, traditional fishman karate robes, helmsman',                              FALSE),
-- Roger Pirates era
('Silvers Rayleigh',                 78, '1945-05-13', 'Male',   'Silver hair, round glasses, scar over right eye, old but impossibly powerful, dark king',                             TRUE),
('Scopper Gaban',                    54, '1969-07-07', 'Male',   'Axe weapons, scruffy hair, tattoos on both arms, Roger pirates officer',                                               FALSE),
-- Other notable pirates
('Nami',                             20, '2003-07-03', 'Female', 'Orange hair, tattoo of pinwheel and mikan on left shoulder, climate baton, ex-Arlong navigator',                      TRUE),
('Nico Robin',                       28, '1995-02-06', 'Female', 'Black hair, blue eyes, Poneglyphs tattoos on arms, can sprout limbs anywhere, only Ohara survivor',                   TRUE),
('Usopp',                            19, '2004-04-01', 'Male',   'Long nose, curly black hair, goggles, slingshot weapon, lies constantly as cover',                                     FALSE),
('Vinsmoke Sanji',                   21, '2002-03-02', 'Male',   'Blonde hair covering right eye, black suit, curly eyebrow, leg-based fighter, Vinsmoke royalty',                      TRUE),
('Yamato',                           28, '1995-11-03', 'Female', 'Long white hair, oni horns, traditional Japanese robes, kanabo club, Kaido daughter',                                 FALSE),
('Carrot',                           21, '2002-05-24', 'Female', 'White rabbit ears, orange eyes, bunny features, electro ability, Sulong moon transformation',                         FALSE),
('Buggy the Clown',                  39, '1984-08-08', 'Male',   'Red nose, blue hair divided by line, clown makeup, detachable body parts, surprisingly feared',                       TRUE),
('Miss All Sunday',                  26, '1998-02-06', 'Female', 'Alias used while with Baroque Works',                                                                                  FALSE),
('Arlong',                           41, '1982-05-03', 'Male',   'Sawshark fishman, blue skin, massive serrated nose, enslaved Cocoyasi village for years',                             TRUE),
('Caesar Clown',                     46, '1977-04-09', 'Male',   'Mad scientist appearance, large head, gas mask, lab coat stained with chemicals, WMD creator',                        TRUE),
('Vergo',                            41, '1982-10-06', 'Male',   'Tall, business attire, bamboo staff, food always stuck to face, Doflamingo spy in marines',                           TRUE),
('Monet',                            25, '1998-01-01', 'Female', 'Harpy wings, snow-white feathers, glasses, Doflamingo tattoo on wrist, logia snow powers',                            FALSE),
('Trebol',                           52, '1971-03-18', 'Male',   'Disgusting mucus-covered body, long cloak, stick weapon, Beta Beta no Mi sticky substance',                           TRUE);

-- ============================================================
-- NICKNAMES
-- ============================================================

INSERT INTO Nickname (criminal_id, alias) VALUES
-- Whitebeard
(1,  'The Strongest Man in the World'),
(1,  'Pops'),
-- Kaido
(2,  'King of the Beasts'),
(2,  'The Strongest Creature'),
-- Big Mom
(3,  'Big Mom'),
(3,  'Mama'),
-- Shanks
(4,  'Red-Hair'),
(4,  'Lucky Man'),
-- Blackbeard
(5,  'Blackbeard'),
(5,  'The Dark King Killer'),
-- Marco
(6,  'Marco the Phoenix'),
-- Ace
(7,  'Fire Fist Ace'),
(7,  'Portgas'),
-- King
(11, 'The Wildfire'),
(11, 'Last Lunarian'),
-- Jack
(12, 'Jack the Drought'),
-- Katakuri
(15, 'Charlotte Katakuri'),
(15, 'The Sweet Commander'),
-- Luffy
(24, 'Straw Hat Luffy'),
(24, 'Fifth Emperor'),
-- Zoro
(25, 'Pirate Hunter Zoro'),
-- Law
(26, 'The Surgeon of Death'),
-- Kid
(27, 'Captain Kid'),
-- Mihawk
(35, 'Hawkeye'),
(35, 'Greatest Swordsman Alive'),
-- Crocodile
(36, 'Desert King'),
(36, 'Mr. Zero'),
-- Doflamingo
(37, 'Heavenly Demon'),
(37, 'Joker'),
-- Rayleigh
(41, 'Dark King'),
(41, 'The Dark King Rayleigh'),
-- Robin
(43, 'Devil Child'),
(43, 'Light of the Revolution'),
-- Buggy
(48, 'Buggy the Star Clown'),
-- Arlong
(49, 'Saw-Tooth Arlong'),
-- Caesar
(50, 'Gas Tank'),
(50, 'Master'),
-- Trebol
(52, 'The Sticky King');

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
(1,  'Firearm',       'Black 9mm handgun found near dumpster'),
(1,  'CCTV Footage',  'Store security camera footage of suspect'),
(2,  'Crowbar',       'Used to force open back window'),
(3,  'Narcotics',     '2kg of cocaine in sealed bags'),
(3,  'Mobile Phone',  'Burner phone with transaction records'),
(4,  'Firearm',       'Pistol recovered at scene'),
(5,  'Laptop',        'Laptop with phishing software installed'),
(6,  'Knife',         '6 inch blade with fingerprints'),
(7,  'Crowbar',       'Found at warehouse entrance'),
(8,  'Narcotics',     '5kg of heroin in checked luggage'),
(9,  'Laptop',        'Used to send phishing emails'),
(10, 'Firearm',       'Sawn-off shotgun left at scene');

-- ============================================================
-- INVESTIGATES (Officer <-> Crime)
-- officer_id: 1=Sengoku, 2=Garp, 3=Aokiji, 4=Sakazuki, 5=Borsalino
--             6=Smoker,  7=Issho, 8=Coby,   9=Tashigi, 10=Tsuru
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
-- criminal_id references:
--  2=Kaido, 5=Blackbeard, 11=King, 15=Katakuri,
-- 24=Luffy, 36=Crocodile, 37=Doflamingo, 50=Caesar
-- ============================================================

INSERT INTO CrimeInvolvement (criminal_id, crime_id) VALUES
(2,  1),   -- Kaido -> armed robbery
(2,  4),   -- Kaido -> carjacking
(2,  10),  -- Kaido -> bank robbery
(5,  2),   -- Blackbeard -> break-in
(5,  7),   -- Blackbeard -> warehouse robbery
(37, 5),   -- Doflamingo -> online fraud
(37, 9),   -- Doflamingo -> phishing ring
(36, 3),   -- Crocodile -> drug deal
(36, 8),   -- Crocodile -> drug trafficking
(50, 5),   -- Caesar -> online fraud (WMD formula leak)
(11, 6),   -- King -> assault
(11, 4),   -- King -> carjacking
(1,  10),  -- Whitebeard -> bank robbery
(49, 7);   -- Arlong -> warehouse robbery

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
(2,  '2024-01-06', 'Active'),    -- Kaido
(5,  '2024-01-09', 'Active'),    -- Blackbeard
(36, '2024-01-10', 'Active'),    -- Crocodile
(11, '2024-01-16', 'Active'),    -- King
(37, '2023-11-01', 'Cancelled'), -- Doflamingo (warrant cancelled - bribed officials)
(1,  '2024-01-24', 'Active'),    -- Whitebeard
(49, '2023-09-15', 'Cancelled'), -- Arlong
(15, '2024-01-20', 'Active'),    -- Katakuri
(50, '2024-01-22', 'Active'),    -- Caesar Clown
(24, '2024-01-15', 'Active');    -- Luffy

-- ============================================================
-- INTERROGATIONS
-- ============================================================

INSERT INTO Interrogation (officer_id, criminal_id, date, notes) VALUES
(1,  2,  '2024-01-07 10:00:00', 'Kaido refused to cooperate. Destroyed the interrogation table. Inconsistent alibi about whereabouts on night of robbery.'),
(4,  5,  '2024-01-10 14:00:00', 'Blackbeard refused to answer questions. Laughed throughout. No lawyer present — he doesnt believe he needs one.'),
(2,  36, '2024-01-11 09:30:00', 'Crocodile admitted to being in the area but denied drug involvement. Extremely calm, suspicious composure.'),
(8,  37, '2024-01-14 11:00:00', 'Doflamingo smiled the entire time. Provided no useful information but mentioned he has friends in high places.'),
(5,  11, '2024-01-16 15:00:00', 'King was aggressive. Broke the cuffs. Denied all charges. No useful information obtained. Extreme threat level noted.'),
(1,  24, '2024-01-24 10:00:00', 'Luffy claimed he just wanted to find treasure. Willing to cooperate if given meat. Surprisingly honest demeanor.');

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
