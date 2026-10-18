-- =============================================================
--  STUDENT PERFORMANCE & PLACEMENT ANALYTICS
--  SQL Analysis Queries
-- =============================================================
--  These queries run against the 'students' table in SQLite.
--  Each query has a comment explaining WHAT / WHY / CONCEPTS.
--  Dataset is ENTIRELY SYNTHETIC / FICTIONAL.
-- =============================================================


-- ─────────────────────────────────────────────────────────────
-- QUERY 1: Total number of students
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Count all student records.
-- WHY    : Establishes the total population for percentage
--          calculations.
-- CONCEPTS: COUNT, aggregate function.
-- ─────────────────────────────────────────────────────────────

SELECT COUNT(*) AS total_students
FROM students;


-- ─────────────────────────────────────────────────────────────
-- QUERY 2: Total placed students
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Count students with Placement_Status = 'Placed'.
-- WHY    : Needed to compute placement rate.
-- CONCEPTS: COUNT, WHERE clause, filtering.
-- ─────────────────────────────────────────────────────────────

SELECT COUNT(*) AS placed_students
FROM students
WHERE Placement_Status = 'Placed';


-- ─────────────────────────────────────────────────────────────
-- QUERY 3: Overall placement percentage
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Compute placement rate as a percentage.
-- WHY    : The single most important KPI.
-- CONCEPTS: ROUND, CAST, subquery, arithmetic in SQL.
-- ─────────────────────────────────────────────────────────────

SELECT
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_percentage
FROM students;


-- ─────────────────────────────────────────────────────────────
-- QUERY 4: Average CGPA of all students
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Compute overall mean CGPA.
-- WHY    : Baseline academic metric.
-- CONCEPTS: AVG, ROUND.
-- ─────────────────────────────────────────────────────────────

SELECT ROUND(AVG(CGPA), 2) AS avg_cgpa
FROM students;


-- ─────────────────────────────────────────────────────────────
-- QUERY 5: Average salary of placed students
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Mean salary where Placement_Status = 'Placed'.
-- WHY    : Key outcome metric for placed students.
-- CONCEPTS: AVG, WHERE, NULL handling (non-placed have NULL salary).
-- ─────────────────────────────────────────────────────────────

SELECT ROUND(AVG(Salary_LPA), 2) AS avg_salary_lpa
FROM students
WHERE Placement_Status = 'Placed';


-- ─────────────────────────────────────────────────────────────
-- QUERY 6: Placement rate by branch
-- ─────────────────────────────────────────────────────────────
-- WHAT   : For each branch, compute total students, placed
--          students, and placement percentage.
-- WHY    : Identifies which branches perform best in placements.
-- CONCEPTS: GROUP BY, CASE, SUM, COUNT, ORDER BY.
-- ─────────────────────────────────────────────────────────────

SELECT
    Branch,
    COUNT(*) AS total,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS placed,
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_rate
FROM students
GROUP BY Branch
ORDER BY placement_rate DESC;


-- ─────────────────────────────────────────────────────────────
-- QUERY 7: Placement rate based on internship status
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Compare placement rates for students with/without
--          internship experience.
-- WHY    : Quantify internship's association with placement.
-- CONCEPTS: GROUP BY, CASE, conditional aggregation.
-- ─────────────────────────────────────────────────────────────

SELECT
    Internship,
    COUNT(*) AS total,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS placed,
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_rate
FROM students
GROUP BY Internship
ORDER BY placement_rate DESC;


-- ─────────────────────────────────────────────────────────────
-- QUERY 8: Placement rate based on backlogs
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Compare students with 0 backlogs vs 1+ backlogs.
-- WHY    : Understand the impact of academic backlogs on
--          placement outcomes.
-- CONCEPTS: CASE for creating categories, GROUP BY.
-- ─────────────────────────────────────────────────────────────

SELECT
    CASE WHEN Backlogs = 0 THEN 'No Backlogs' ELSE 'Has Backlogs' END AS backlog_status,
    COUNT(*) AS total,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS placed,
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_rate
FROM students
GROUP BY backlog_status
ORDER BY placement_rate DESC;


-- ─────────────────────────────────────────────────────────────
-- QUERY 9: Top 10 students by composite performance
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Rank students using a weighted composite score.
-- WHY    : Identifies high performers across multiple criteria.
-- CONCEPTS: Arithmetic expressions, ORDER BY, LIMIT, ROUND.
-- ─────────────────────────────────────────────────────────────

SELECT
    Student_ID,
    Branch,
    CGPA,
    Technical_Score,
    Aptitude_Score,
    Communication_Score,
    Placement_Status,
    Salary_LPA,
    ROUND(
        CGPA * 10               -- normalise to 100
        + Technical_Score * 0.3
        + Aptitude_Score * 0.2
        + Communication_Score * 0.2
        + Number_of_Projects * 5
        + Certifications * 3,
        2
    ) AS composite_score
FROM students
ORDER BY composite_score DESC
LIMIT 10;


-- ─────────────────────────────────────────────────────────────
-- QUERY 10: Salary statistics by branch (placed students)
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Min, max, average, and median-approximation salary
--          for each branch.
-- WHY    : Compare salary offerings across branches.
-- CONCEPTS: MIN, MAX, AVG, GROUP BY, WHERE.
-- ─────────────────────────────────────────────────────────────

SELECT
    Branch,
    COUNT(*) AS placed_count,
    ROUND(MIN(Salary_LPA), 2) AS min_salary,
    ROUND(AVG(Salary_LPA), 2) AS avg_salary,
    ROUND(MAX(Salary_LPA), 2) AS max_salary
FROM students
WHERE Placement_Status = 'Placed'
GROUP BY Branch
ORDER BY avg_salary DESC;


-- ─────────────────────────────────────────────────────────────
-- QUERY 11: Placement rate by CGPA range
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Group students into CGPA buckets and compute
--          placement rates for each.
-- WHY    : Shows how academic performance tiers relate to
--          placement outcomes.
-- CONCEPTS: CASE for bucketing, GROUP BY, ORDER BY.
-- ─────────────────────────────────────────────────────────────

SELECT
    CASE
        WHEN CGPA < 5 THEN '< 5.0'
        WHEN CGPA < 6 THEN '5.0 – 5.9'
        WHEN CGPA < 7 THEN '6.0 – 6.9'
        WHEN CGPA < 8 THEN '7.0 – 7.9'
        WHEN CGPA < 9 THEN '8.0 – 8.9'
        ELSE '9.0 – 10.0'
    END AS cgpa_range,
    COUNT(*) AS total,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS placed,
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_rate
FROM students
GROUP BY cgpa_range
ORDER BY cgpa_range;


-- ─────────────────────────────────────────────────────────────
-- QUERY 12: Placement rate by project count
-- ─────────────────────────────────────────────────────────────
-- WHAT   : For each project count (0–5), compute placement %.
-- WHY    : Shows whether project experience is associated with
--          better placement chances.
-- CONCEPTS: GROUP BY on integer column, ORDER BY.
-- ─────────────────────────────────────────────────────────────

SELECT
    Number_of_Projects,
    COUNT(*) AS total,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS placed,
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_rate
FROM students
GROUP BY Number_of_Projects
ORDER BY Number_of_Projects;


-- ─────────────────────────────────────────────────────────────
-- QUERY 13 (BONUS): Average scores — Placed vs Not Placed
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Side-by-side average of key scores for placed vs
--          non-placed students.
-- WHY    : Highlights which skill areas differ most.
-- CONCEPTS: GROUP BY, AVG, multiple aggregations.
-- ─────────────────────────────────────────────────────────────

SELECT
    Placement_Status,
    COUNT(*) AS count,
    ROUND(AVG(CGPA), 2) AS avg_cgpa,
    ROUND(AVG(Technical_Score), 2) AS avg_tech,
    ROUND(AVG(Aptitude_Score), 2) AS avg_apt,
    ROUND(AVG(Communication_Score), 2) AS avg_comm,
    ROUND(AVG(Resume_Score), 2) AS avg_resume,
    ROUND(AVG(Attendance_Percentage), 2) AS avg_attendance
FROM students
GROUP BY Placement_Status;


-- ─────────────────────────────────────────────────────────────
-- QUERY 14 (BONUS): Placement rate by gender and branch
-- ─────────────────────────────────────────────────────────────
-- WHAT   : Cross-tabulation of gender × branch placement rates.
-- WHY    : Multi-dimensional analysis useful for dashboards.
-- CONCEPTS: Multiple GROUP BY columns, HAVING (optional).
-- ─────────────────────────────────────────────────────────────

SELECT
    Gender,
    Branch,
    COUNT(*) AS total,
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS placed,
    ROUND(
        CAST(SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) AS REAL)
        / COUNT(*) * 100,
        2
    ) AS placement_rate
FROM students
GROUP BY Gender, Branch
ORDER BY Gender, placement_rate DESC;
