-- Create the Student Club Management database
CREATE DATABASE IF NOT EXISTS Student_Club_Management;

-- Use the Student Club Management database
USE Student_Club_Management;

-- Table: Students
CREATE TABLE IF NOT EXISTS Students (
    StudentID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Email NVARCHAR(100) UNIQUE
);

-- Table: Admin
CREATE TABLE IF NOT EXISTS Admin (
    AdminID INT PRIMARY KEY,
    FirstName NVARCHAR(50),
    LastName NVARCHAR(50),
    Email NVARCHAR(100) UNIQUE
);

-- Table: Clubs
CREATE TABLE IF NOT EXISTS Clubs (
    ClubID INT PRIMARY KEY,
    ClubName NVARCHAR(100) UNIQUE,
    Description NVARCHAR(MAX)
);

-- Table: Club_Members
CREATE TABLE IF NOT EXISTS Club_Members (
    MemberID INT PRIMARY KEY,
    StudentID INT,
    ClubID INT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);

-- Table: Events
CREATE TABLE IF NOT EXISTS Events (
    EventID INT PRIMARY KEY,
    EventName NVARCHAR(100),
    Date DATE,
    Description NVARCHAR(MAX)
);

-- Table: Events_Club
CREATE TABLE IF NOT EXISTS Events_Club (
    EventID INT,
    ClubID INT,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID)
);

-- Table: Event_Admin
CREATE TABLE IF NOT EXISTS Event_Admin (
    EventID INT,
    AdminID INT,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (AdminID) REFERENCES Admin(AdminID)
);

-- Table: Event_Participants
CREATE TABLE IF NOT EXISTS Event_Participants (
    EventID INT,
    StudentID INT,
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- Table: Club_Leaders
CREATE TABLE IF NOT EXISTS Club_Leaders (
    ClubID INT,
    PresidentID INT,
    VicePresidentID INT,
    SecretaryID INT,
    PRIMARY KEY (ClubID, PresidentID, VicePresidentID, SecretaryID),
    FOREIGN KEY (ClubID) REFERENCES Clubs(ClubID),
    FOREIGN KEY (PresidentID) REFERENCES Students(StudentID),
    FOREIGN KEY (VicePresidentID) REFERENCES Students(StudentID),
    FOREIGN KEY (SecretaryID) REFERENCES Students(StudentID)
);
