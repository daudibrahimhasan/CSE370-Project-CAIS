# <h1 align = "center"> Database Queries </h1>
## 00. Create & Use Database
```sql
CREATE DATABASE project_database;
USE project_database;
```

## 01. Create ADMIN table
```sql
CREATE TABLE admin (
    AdminID INT PRIMARY KEY AUTO_INCREMENT,
    Username VARCHAR(150) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL,
    Role ENUM('Admin', 'Viewer') NOT NULL DEFAULT 'Viewer',
    IsActive TINYINT(1) NOT NULL DEFAULT 1,
    CreatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## 02. Create TEAM table
```sql
CREATE TABLE team (
    TeamID INT PRIMARY KEY AUTO_INCREMENT,
    TeamName VARCHAR(100) UNIQUE NOT NULL
);
```

## 03. Create OFFICER table
```sql
CREATE TABLE officer (
    OfficerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(150) NOT NULL,
    RankName VARCHAR(100) NOT NULL,
    BadgeNumber VARCHAR(50) UNIQUE NOT NULL,
    TeamID INT NULL,
    FOREIGN KEY (TeamID) REFERENCES team(TeamID) ON DELETE SET NULL
);
```

## 04. Create OFFICER_SHIFT table
```sql
CREATE TABLE officer_shift (
    ShiftID INT PRIMARY KEY AUTO_INCREMENT,
    OfficerID INT NOT NULL,
    ShiftDate DATE NOT NULL,
    HoursWorked DECIMAL(4,2) NOT NULL,
    FOREIGN KEY (OfficerID) REFERENCES officer(OfficerID) ON DELETE CASCADE
);
```

## 05. Create CRIMINAL table
```sql
CREATE TABLE criminal (
    CriminalID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(150) NOT NULL,
    Age INT NOT NULL,
    DateOfBirth DATE DEFAULT NULL,
    Gender VARCHAR(50) NOT NULL,
    PhysicalDescription TEXT NOT NULL,
    IsRepeatOffender TINYINT(1) NOT NULL DEFAULT 0
);
```

## 06. Create CRIMINAL_NICKNAME table
```sql
CREATE TABLE criminal_nickname (
    NicknameID INT PRIMARY KEY AUTO_INCREMENT,
    CriminalID INT NOT NULL,
    AliasName VARCHAR(100) NOT NULL,
    FOREIGN KEY (CriminalID) REFERENCES criminal(CriminalID) ON DELETE CASCADE
);
```

## 07. Create INTERROGATION table
```sql
CREATE TABLE interrogation (
    InterrogationID INT PRIMARY KEY AUTO_INCREMENT,
    OfficerID INT NULL,
    CriminalID INT NOT NULL,
    QuestionedAt DATETIME NOT NULL,
    Notes TEXT NOT NULL,
    FOREIGN KEY (OfficerID) REFERENCES officer(OfficerID) ON DELETE SET NULL,
    FOREIGN KEY (CriminalID) REFERENCES criminal(CriminalID) ON DELETE CASCADE
);
```

## 08. Create VICTIM table
```sql
CREATE TABLE victim (
    VictimID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(150) NOT NULL
);
```

## 09. Create VICTIM_PHONE table
```sql
CREATE TABLE victim_phone (
    PhoneID INT PRIMARY KEY AUTO_INCREMENT,
    VictimID INT NOT NULL,
    PhoneNumber VARCHAR(20) NOT NULL,
    FOREIGN KEY (VictimID) REFERENCES victim(VictimID) ON DELETE CASCADE
);
```

## 10. Create CRIME table
```sql
CREATE TABLE crime (
    CrimeID INT PRIMARY KEY AUTO_INCREMENT,
    Description TEXT NOT NULL,
    MethodUsed VARCHAR(255) NOT NULL,
    LocationName VARCHAR(255) NOT NULL,
    City VARCHAR(150) DEFAULT NULL,
    Latitude DECIMAL(9,6) DEFAULT NULL,
    Longitude DECIMAL(9,6) DEFAULT NULL,
    OccurredAt DATETIME NOT NULL,
    CrimeStatus ENUM('Open', 'Closed', 'Cold') NOT NULL DEFAULT 'Open'
);
```

## 11. Create EVIDENCE table
```sql
CREATE TABLE evidence (
    EvidenceID INT PRIMARY KEY AUTO_INCREMENT,
    CrimeID INT NOT NULL,
    EvidenceType VARCHAR(100) NOT NULL,
    Description TEXT NOT NULL,
    FOREIGN KEY (CrimeID) REFERENCES crime(CrimeID) ON DELETE CASCADE
);
```

## 12. Create CRIME_INVOLVEMENT table
```sql
CREATE TABLE crime_involvement (
    InvolvementID INT PRIMARY KEY AUTO_INCREMENT,
    CriminalID INT NOT NULL,
    CrimeID INT NOT NULL,
    UNIQUE KEY uq_crime_involvement (CriminalID, CrimeID),
    FOREIGN KEY (CriminalID) REFERENCES criminal(CriminalID) ON DELETE CASCADE,
    FOREIGN KEY (CrimeID) REFERENCES crime(CrimeID) ON DELETE CASCADE
);
```

## 13. Create CRIME_VICTIM table
```sql
CREATE TABLE crime_victim (
    CrimeVictimID INT PRIMARY KEY AUTO_INCREMENT,
    CrimeID INT NOT NULL,
    VictimID INT NOT NULL,
    UNIQUE KEY uq_crime_victim (CrimeID, VictimID),
    FOREIGN KEY (CrimeID) REFERENCES crime(CrimeID) ON DELETE CASCADE,
    FOREIGN KEY (VictimID) REFERENCES victim(VictimID) ON DELETE CASCADE
);
```

## 14. Create INVESTIGATES table
```sql
CREATE TABLE investigates (
    InvestigationID INT PRIMARY KEY AUTO_INCREMENT,
    OfficerID INT NOT NULL,
    CrimeID INT NOT NULL,
    WorkDate DATE NOT NULL,
    UNIQUE KEY uq_investigates (OfficerID, CrimeID, WorkDate),
    FOREIGN KEY (OfficerID) REFERENCES officer(OfficerID) ON DELETE CASCADE,
    FOREIGN KEY (CrimeID) REFERENCES crime(CrimeID) ON DELETE CASCADE
);
```

## 15. Create WARRANT table
```sql
CREATE TABLE warrant (
    WarrantID INT PRIMARY KEY AUTO_INCREMENT,
    CriminalID INT NOT NULL,
    IssueDate DATE NOT NULL,
    WarrantStatus ENUM('Active', 'Cancelled') NOT NULL DEFAULT 'Active',
    FOREIGN KEY (CriminalID) REFERENCES criminal(CriminalID) ON DELETE CASCADE
);
```

## 16. Create CASE_RECORD table
```sql
CREATE TABLE case_record (
    CaseID INT PRIMARY KEY AUTO_INCREMENT,
    CrimeID INT NOT NULL UNIQUE,
    CaseStatus ENUM('Open', 'Finished') NOT NULL DEFAULT 'Open',
    OpenedDate DATE DEFAULT NULL,
    FOREIGN KEY (CrimeID) REFERENCES crime(CrimeID) ON DELETE CASCADE
);
```

## 17. Create COURT_DATE table
```sql
CREATE TABLE court_date (
    CourtID INT PRIMARY KEY AUTO_INCREMENT,
    CaseID INT NOT NULL,
    CourtDate DATE NOT NULL,
    JudgeName VARCHAR(150) NOT NULL,
    FOREIGN KEY (CaseID) REFERENCES case_record(CaseID) ON DELETE CASCADE
);
```

## 18. Crime Pattern Finder View
```sql
CREATE VIEW crime_pattern_finder AS
SELECT
    MethodUsed,
    COUNT(*) AS TotalCrimes,
    GROUP_CONCAT(CrimeID ORDER BY OccurredAt SEPARATOR ', ') AS CrimeIDs
FROM crime
GROUP BY MethodUsed
ORDER BY TotalCrimes DESC, MethodUsed;
```

## 19. Repeat Offender Alert View
```sql
CREATE VIEW repeat_offender_alert AS
SELECT
    c.CriminalID,
    c.Name,
    COUNT(ci.CrimeID) AS ArrestCount,
    CASE
        WHEN COUNT(ci.CrimeID) >= 2 THEN 'Repeat Criminal'
        ELSE 'Single Record'
    END AS RepeatStatus
FROM criminal c
LEFT JOIN crime_involvement ci ON c.CriminalID = ci.CriminalID
GROUP BY c.CriminalID, c.Name
ORDER BY ArrestCount DESC, c.Name;
```

## 20. BOLO List View
```sql
CREATE VIEW bolo_list AS
SELECT
    w.WarrantID,
    w.IssueDate,
    c.CriminalID,
    c.Name,
    c.Age,
    c.Gender,
    c.PhysicalDescription
FROM warrant w
JOIN criminal c ON w.CriminalID = c.CriminalID
WHERE w.WarrantStatus = 'Active'
ORDER BY w.IssueDate DESC;
```

## 21. Officer Search Query
```sql
SELECT o.OfficerID, o.Name, o.RankName, o.BadgeNumber, t.TeamName
FROM officer o
LEFT JOIN team t ON o.TeamID = t.TeamID
WHERE o.RankName = 'Detective' OR t.TeamName = 'Narcotics';
```

## 22. Crime Pattern Search Query
```sql
SELECT CrimeID, Description, MethodUsed, LocationName, OccurredAt
FROM crime
WHERE MethodUsed LIKE '%same trick%'
ORDER BY OccurredAt DESC;
```

## 23. Repeat Offender Counting Query
```sql
SELECT c.CriminalID, c.Name, COUNT(ci.CrimeID) AS ArrestCount
FROM criminal c
JOIN crime_involvement ci ON c.CriminalID = ci.CriminalID
GROUP BY c.CriminalID, c.Name
HAVING COUNT(ci.CrimeID) >= 2;
```

## 24. Case and Court Tracking Query
```sql
SELECT cr.CaseID, cr.CaseStatus, c.CrimeID, c.Description, cd.CourtDate, cd.JudgeName
FROM case_record cr
JOIN crime c ON cr.CrimeID = c.CrimeID
LEFT JOIN court_date cd ON cr.CaseID = cd.CaseID;
```
