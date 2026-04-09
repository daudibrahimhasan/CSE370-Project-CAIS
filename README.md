# Criminal Analysis & Investigation System (CAIS)

Course Code: CSE370

A robust, law-enforcement web application built to track criminal profiles, manage investigations, log evidence, and identify crime patterns using advanced data relationships.

## ✨ Overview

CAIS helps police departments and administrators organize officer squads, track repeat offenders, match crime patterns (M.O.), and maintain secure chains of evidence—ensuring public safety and more efficient investigations.

### 📸 Project Preview
![Login System](public/1.png)
![System Dashboard](public/2.png)
![Active BOLOs](public/3.png)
![Case Management](public/4.png)
![Criminal Registry](public/5.png)
![Crime Patterns](public/6.png)
![System Personnel](public/7.png)
![Warrant Tracking](public/8.png)

- 🗺️ **Crime Pattern Finder** (links crimes with the same method/trick)

- 📚 **Repeat Offender Alerts** (automatically flags high-frequency criminals)
- 📝 **Warrants & BOLO** (Be On the Lookout) tracking for public safety
- 👥 **Officer & Team** tracking (manage shifts, divisions, and ranks)
- 🛠️ **Master Criminal Index** & interrogation logs
- 🏛️ **Case and Court Date** management

## 📦 Tech Stack

- **Frontend:** HTML, CSS (Tailwind), Vanilla JavaScript
- **Backend:** Python (Django Framework)
- **Database:** MySQL / SQLite

## 🧩 Feature Matrix

| Sl  | Feature Name                | Type                 | Notes                                                             |
| --- | --------------------------- | -------------------- | ----------------------------------------------------------------- |
| 1   | **Admin Authentication**    | —                    | Secure session-based login for authorized personnel only.         |
| 2   | **Officer Directory**       | Create, Read, Update | Manage officer names, ranks, and badge numbers.                   |
| 3   | **Team Management**         | Create, Read, Update | Assign officers to specific squads (e.g., Homicide, Narcotics).   |
| 4   | **Criminal Registry**       | Create, Read, Update | Store physical traits, age, gender, and profile status.           |
| 5   | **Alias/Nickname Tracking** | Create, Read, Delete | Record and manage multiple street names per subject.              |
| 6   | **Warrant Tracking**        | Create, Read, Update | Track "Active" or "Cancelled" bench warrants.                     |
| 7   | **BOLO List**               | Read                 | Specialized view filtering only 'Active' warrants.                |
| 8   | **Crime Records**           | Create, Read, Update | Log locations, dates, and methods of operation (M.O.).            |
| 9   | **Crime Pattern Finder**    | Read                 | Identify linked crimes sharing the same operational tactics.      |
| 10  | **Evidence Vault**          | Create, Read, Delete | Attach weapons, devices, and physical items to specific cases.    |
| 11  | **Victim Roster**           | Create, Read, Update | Store affected individuals' names and secure contact numbers.     |
| 12  | **Case Lifecycle**          | Create, Read, Update | Manage case status (e.g., "Open" or "Finished").                  |
| 13  | **Legal Calendar**          | Create, Read, Update | Track court appearance dates and presiding judges.                |
| 14  | **Repeat Offender Alert**   | Read                 | Aggregates crime counts to automatically flag habitual offenders. |
| 15  | **Interrogation Logs**      | Create, Read, Update | Store private interview notes between officers and suspects.      |

## 👥 Team

- **Daud Ibrahim Hassan**
- **Abir Enam**
- **Ocean Biswas**
