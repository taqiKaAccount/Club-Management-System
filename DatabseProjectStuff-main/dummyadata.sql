CREATE TABLE [dbo].[CLUBS](
    [CLUB_ID] INTEGER PRIMARY KEY IDENTITY,
    [CLUB_NAME] VARCHAR(255),
    [DESCRIPTION] TEXT,
    [FUNDS] INTEGER,
    [member_count] INTEGER,
    [club_size] INTEGER
);

CREATE TABLE [dbo].[STUDENTS](
    [STUDENT_ID] INTEGER PRIMARY KEY IDENTITY,
    [STUDENT_NAME] TEXT,
    [STUDENT_EMAIL] VARCHAR(255),
    [PASSWORD] VARCHAR(255),
    [BATCH] INTEGER
);

CREATE TABLE [dbo].[CLUB_MEMBERS](
    [CLUB_ID] INTEGER,
    [STUDENT_ID] INTEGER,
    [Joined_Date] DATETIME,
    [Events_Organised] INTEGER,
    PRIMARY KEY ([CLUB_ID], [STUDENT_ID]),
    FOREIGN KEY ([CLUB_ID]) REFERENCES [dbo].[CLUBS]([CLUB_ID]),
    FOREIGN KEY ([STUDENT_ID]) REFERENCES [dbo].[STUDENTS]([STUDENT_ID])
);

CREATE TABLE [dbo].[ADMIN](
    [ADMIN_ID] INTEGER PRIMARY KEY IDENTITY,
    [ADMIN_NAME] VARCHAR(255),
    [ADMIN_EMAIL] VARCHAR(255),
    [ADMIN_PASSWORD] VARCHAR(255),
    [ROLE] INTEGER
);

CREATE TABLE [dbo].[Club_Leadership](
    [Club_ID] INTEGER,
    [president] INTEGER,
    [vice_president] INTEGER,
    [secretary] INTEGER,
    PRIMARY KEY ([Club_ID]),
    FOREIGN KEY ([Club_ID]) REFERENCES [dbo].[CLUBS]([CLUB_ID]),
    FOREIGN KEY ([president]) REFERENCES [dbo].[STUDENTS]([STUDENT_ID]),
    FOREIGN KEY ([vice_president]) REFERENCES [dbo].[STUDENTS]([STUDENT_ID]),
    FOREIGN KEY ([secretary]) REFERENCES [dbo].[STUDENTS]([STUDENT_ID])
);

CREATE TABLE [dbo].[EVENTS](
    [DATE] DATE,
    [TIME] TEXT,
    [EVENT_NAME] VARCHAR(255),
    [EVENT_ID] INTEGER PRIMARY KEY IDENTITY,
    [Organising_Club] INTEGER,
    [LOCATION] TEXT,
    [Funds_Used] INTEGER,
    FOREIGN KEY ([Organising_Club]) REFERENCES [dbo].[CLUBS]([CLUB_ID])
);

CREATE TABLE [dbo].[event_participants](
    [participation_id] INTEGER PRIMARY KEY IDENTITY,
    [student_id] INTEGER,
    [event_id] INTEGER,
    [registrationDate] DATETIME,
    FOREIGN KEY ([student_id]) REFERENCES [dbo].[STUDENTS]([STUDENT_ID]),
    FOREIGN KEY ([event_id]) REFERENCES [dbo].[EVENTS]([EVENT_ID])
);

CREATE TABLE [dbo].[Events_Clubs](
    [Club_ID] INTEGER,
    [Events_ID] INTEGER,
    PRIMARY KEY ([Club_ID], [Events_ID]),
    FOREIGN KEY ([Club_ID]) REFERENCES [dbo].[CLUBS]([CLUB_ID]),
    FOREIGN KEY ([Events_ID]) REFERENCES [dbo].[EVENTS]([EVENT_ID])
);

CREATE TABLE [dbo].[EVENT_ADMIN](
    [ADMIN_ID] INTEGER,
    [EVENT_ID] INTEGER,
    PRIMARY KEY ([ADMIN_ID], [EVENT_ID]),
    FOREIGN KEY ([ADMIN_ID]) REFERENCES [dbo].[ADMIN]([ADMIN_ID]),
    FOREIGN KEY ([EVENT_ID]) REFERENCES [dbo].[EVENTS]([EVENT_ID])
);

INSERT INTO [dbo].[CLUBS] ([CLUB_ID], [CLUB_NAME], [DESCRIPTION], [FUNDS], [member_count], [club_size])
VALUES 
(1, 'Chess Club', 'A club for chess enthusiasts', 500, 20, 30),
(2, 'Debate Society', 'Promoting public speaking and debating skills', 800, 15, 25),
(3, 'Photography Club', 'Exploring the art of photography', 600, 25, 35);

INSERT INTO [dbo].[STUDENTS] ([STUDENT_ID], [STUDENT_NAME], [STUDENT_EMAIL], [PASSWORD], [BATCH])
VALUES 
(1, 'Alice', 'alice@example.com', 'password123', 2022),
(2, 'Bob', 'bob@example.com', 'password456', 2023),
(3, 'Charlie', 'charlie@example.com', 'password789', 2022);

INSERT INTO [dbo].[CLUB_MEMBERS] ([CLUB_ID], [STUDENT_ID], [Joined_Date], [Events_Organised])
VALUES 
(1, 1, '2023-01-15 10:00:00', 5),
(1, 3, '2023-02-20 11:30:00', 3),
(2, 2, '2023-03-10 09:45:00', 4);

INSERT INTO [dbo].[Club_Leadership] ([Club_ID], [president], [vice_president], [secretary])
VALUES 
(1, 1, 3, NULL),
(2, 2, NULL, NULL);

INSERT INTO [dbo].[EVENTS] ([DATE], [TIME], [EVENT_NAME], [Organising_Club], [LOCATION], [Funds_Used])
VALUES 
('2023-06-25', '15:00:00', 'Chess Tournament', 1, 'Auditorium A', 200),
('2023-07-10', '14:30:00', 'Debate Competition', 2, 'Conference Hall', 300);

INSERT INTO [dbo].[event_participants] ([student_id], [event_id], [registrationDate])
VALUES 
(1, 1, '2023-06-10 08:00:00'),
(2, 2, '2023-06-28 09:30:00'),
(3, 1, '2023-06-15 11:45:00');

INSERT INTO [dbo].[Events_Clubs] ([Club_ID], [Events_ID])
VALUES 
(1, 1),
(2, 2);

INSERT INTO [dbo].[EVENT_ADMIN] ([ADMIN_ID], [EVENT_ID])
VALUES 
(1, 1),
(2, 2);