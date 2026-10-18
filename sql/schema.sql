-- =============================================================
--  STUDENT PERFORMANCE & PLACEMENT ANALYTICS
--  Database Schema (SQLite)
-- =============================================================
--  This creates the 'students' table used for SQL analysis.
--  Dataset is ENTIRELY SYNTHETIC / FICTIONAL.
-- =============================================================

-- Drop table if it already exists (for re-runs)
DROP TABLE IF EXISTS students;

-- Create main table
CREATE TABLE students (
    Student_ID            TEXT PRIMARY KEY,
    Gender                TEXT NOT NULL,
    Age                   INTEGER NOT NULL,
    Branch                TEXT NOT NULL,
    Semester              INTEGER NOT NULL,
    CGPA                  REAL NOT NULL,
    Attendance_Percentage REAL NOT NULL,
    Aptitude_Score        REAL NOT NULL,
    Technical_Score       REAL NOT NULL,
    Communication_Score   REAL NOT NULL,
    Programming_Skills    TEXT,
    Number_of_Projects    INTEGER NOT NULL,
    Certifications        INTEGER NOT NULL,
    Internship            TEXT NOT NULL,       -- 'Yes' / 'No'
    Internship_Months     INTEGER NOT NULL,
    Backlogs              INTEGER NOT NULL,
    Hackathon_Participation TEXT NOT NULL,      -- 'Yes' / 'No'
    Resume_Score          REAL NOT NULL,
    Placement_Training    TEXT NOT NULL,        -- 'Yes' / 'No'
    Placement_Status      TEXT NOT NULL,        -- 'Placed' / 'Not Placed'
    Salary_LPA            REAL                  -- NULL for not-placed students
);

-- Index for common queries
CREATE INDEX idx_placement ON students(Placement_Status);
CREATE INDEX idx_branch    ON students(Branch);
CREATE INDEX idx_internship ON students(Internship);
