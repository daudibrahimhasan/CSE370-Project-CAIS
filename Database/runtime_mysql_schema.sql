-- ============================================================
-- CAIS Runtime MySQL Schema
-- This file reflects the real Django runtime table names used by
-- the current Python view files and raw SQL queries.
-- ============================================================

CREATE DATABASE IF NOT EXISTS Project_database;
USE Project_database;

CREATE TABLE IF NOT EXISTS admin_auth_adminuser (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser TINYINT(1) NOT NULL DEFAULT 0,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff TINYINT(1) NOT NULL DEFAULT 0,
    is_active TINYINT(1) NOT NULL DEFAULT 1,
    date_joined DATETIME NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'Viewer'
);

CREATE TABLE IF NOT EXISTS officers_team (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS officers_officer (
    officer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    rank VARCHAR(100) NOT NULL,
    badge_number VARCHAR(50) NOT NULL UNIQUE,
    team_id INT NULL,
    FOREIGN KEY (team_id) REFERENCES officers_team(team_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS officers_shift (
    shift_id INT AUTO_INCREMENT PRIMARY KEY,
    officer_id INT NOT NULL,
    date DATE NOT NULL,
    hours_worked DECIMAL(4,2) NOT NULL,
    FOREIGN KEY (officer_id) REFERENCES officers_officer(officer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS criminals_criminal (
    criminal_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    age INT NOT NULL,
    date_of_birth DATE NULL,
    gender VARCHAR(50) NOT NULL,
    physical_description TEXT NOT NULL,
    is_repeat_offender TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS criminals_nickname (
    nickname_id INT AUTO_INCREMENT PRIMARY KEY,
    criminal_id INT NOT NULL,
    alias VARCHAR(100) NOT NULL,
    FOREIGN KEY (criminal_id) REFERENCES criminals_criminal(criminal_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS criminals_interrogation (
    interrogation_id INT AUTO_INCREMENT PRIMARY KEY,
    officer_id INT NULL,
    criminal_id INT NOT NULL,
    date DATETIME NOT NULL,
    notes TEXT NOT NULL,
    FOREIGN KEY (officer_id) REFERENCES officers_officer(officer_id) ON DELETE SET NULL,
    FOREIGN KEY (criminal_id) REFERENCES criminals_criminal(criminal_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crimes_victim (
    victim_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL
);

CREATE TABLE IF NOT EXISTS crimes_victimphone (
    phone_id INT AUTO_INCREMENT PRIMARY KEY,
    victim_id INT NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    FOREIGN KEY (victim_id) REFERENCES crimes_victim(victim_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crimes_crime (
    crime_id INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    method_used VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    city VARCHAR(150) NULL,
    latitude DECIMAL(9,6) NULL,
    longitude DECIMAL(9,6) NULL,
    date_time DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Open'
);

CREATE TABLE IF NOT EXISTS crimes_evidence (
    evidence_id INT AUTO_INCREMENT PRIMARY KEY,
    crime_id INT NOT NULL,
    type VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (crime_id) REFERENCES crimes_crime(crime_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crimes_crimeinvolvement (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    criminal_id INT NOT NULL,
    crime_id INT NOT NULL,
    UNIQUE KEY uq_crimes_crimeinvolvement (criminal_id, crime_id),
    FOREIGN KEY (criminal_id) REFERENCES criminals_criminal(criminal_id) ON DELETE CASCADE,
    FOREIGN KEY (crime_id) REFERENCES crimes_crime(crime_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crimes_crimevictim (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    crime_id INT NOT NULL,
    victim_id INT NOT NULL,
    UNIQUE KEY uq_crimes_crimevictim (crime_id, victim_id),
    FOREIGN KEY (crime_id) REFERENCES crimes_crime(crime_id) ON DELETE CASCADE,
    FOREIGN KEY (victim_id) REFERENCES crimes_victim(victim_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS crimes_investigates (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    officer_id INT NOT NULL,
    crime_id INT NOT NULL,
    date_worked DATE NOT NULL,
    UNIQUE KEY uq_crimes_investigates (officer_id, crime_id, date_worked),
    FOREIGN KEY (officer_id) REFERENCES officers_officer(officer_id) ON DELETE CASCADE,
    FOREIGN KEY (crime_id) REFERENCES crimes_crime(crime_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS warrants_warrant (
    warrant_id INT AUTO_INCREMENT PRIMARY KEY,
    criminal_id INT NOT NULL,
    issue_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Active',
    FOREIGN KEY (criminal_id) REFERENCES criminals_criminal(criminal_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS cases_case (
    case_id INT AUTO_INCREMENT PRIMARY KEY,
    crime_id INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Open',
    opened_date DATE NULL,
    FOREIGN KEY (crime_id) REFERENCES crimes_crime(crime_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS court_court (
    court_id INT AUTO_INCREMENT PRIMARY KEY,
    case_id INT NOT NULL,
    court_date DATE NOT NULL,
    judge_name VARCHAR(150) NOT NULL,
    FOREIGN KEY (case_id) REFERENCES cases_case(case_id) ON DELETE CASCADE
);
