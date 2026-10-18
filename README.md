# Student Performance & Placement Analytics

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-green?logo=pandas)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?logo=sqlite)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)
![License](https://img.shields.io/badge/License-MIT-green)

A complete **Data Analytics portfolio project** that analyzes student academic performance, technical skills, internships, certifications, and placement outcomes to identify patterns and factors associated with placement success.

> **Disclaimer:** This project uses a **synthetic (fictional) dataset** generated for educational and portfolio purposes. It does **not** represent any real students, institution, or organization.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Objectives](#objectives)
- [Dataset Description](#dataset-description)
- [Technologies Used](#technologies-used)
- [Project Workflow](#project-workflow)
- [Data Cleaning](#data-cleaning)
- [Exploratory Data Analysis](#exploratory-data-analysis)
- [SQL Analysis](#sql-analysis)
- [Power BI Dashboard](#power-bi-dashboard)
- [Key Insights](#key-insights)
- [Recommendations](#recommendations)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## Project Overview

Campus placements are a critical milestone for engineering students. This project analyzes a synthetic dataset of **1,000 student records** across 6 engineering branches to uncover which factors — CGPA, internships, backlogs, technical scores, certifications, projects — are most strongly associated with placement outcomes and salary levels.

The analysis pipeline covers the complete data analytics lifecycle: data generation, cleaning, exploratory analysis, SQL querying, interactive dashboarding, and actionable insights.

---

## Problem Statement

Educational institutions and students lack a data-driven understanding of which academic and extracurricular factors contribute most to placement success. Without this understanding, students may not know where to focus their efforts, and colleges may not optimally allocate training resources.

---

## Objectives

1. Generate a realistic synthetic student dataset with academic, skill, and placement data
2. Clean and validate the data, handling missing values and inconsistencies
3. Perform exploratory data analysis to discover patterns in placement outcomes
4. Use SQL queries to answer structured analytical questions
5. Design a Power BI dashboard for interactive exploration
6. Derive actionable insights and recommendations for students, colleges, and placement coordinators

---

## Dataset Description

| Column | Type | Description | Range/Values |
|--------|------|-------------|--------------|
| Student_ID | Text | Unique identifier | STU0001–STU1000 |
| Gender | Categorical | Student gender | Male, Female |
| Age | Integer | Student age | 20–24 |
| Branch | Categorical | Engineering branch | CS, IT, Electronics, Mechanical, Civil, Electrical |
| Semester | Integer | Current semester | 7, 8 |
| CGPA | Float | Cumulative GPA | 4.0–10.0 |
| Attendance_Percentage | Float | Class attendance | 40–100% |
| Aptitude_Score | Float | Aptitude test score | 0–100 |
| Technical_Score | Float | Technical assessment | 0–100 |
| Communication_Score | Float | Communication assessment | 0–100 |
| Programming_Skills | Text | Known languages | Python, Java, C++, etc. |
| Number_of_Projects | Integer | Projects completed | 0–5 |
| Certifications | Integer | Certifications earned | 0–5 |
| Internship | Categorical | Has internship experience | Yes, No |
| Internship_Months | Integer | Duration of internship | 0–6 |
| Backlogs | Integer | Active backlogs | 0–3 |
| Hackathon_Participation | Categorical | Participated in hackathons | Yes, No |
| Resume_Score | Float | Resume quality score | 20–100 |
| Placement_Training | Categorical | Attended placement training | Yes, No |
| Placement_Status | Categorical | Placement outcome | Placed, Not Placed |
| Salary_LPA | Float | Annual salary (lakhs) | 2.5–18.0 (NaN if not placed) |

**Size:** 1,000 rows × 21 columns

---

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Python 3.11** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations and random data generation |
| **Matplotlib** | Static data visualizations |
| **Seaborn** | Statistical visualizations |
| **SQLite** | Lightweight SQL database |
| **Power BI** | Interactive dashboard |
| **Git & GitHub** | Version control and portfolio hosting |

---

## Project Workflow

```
Synthetic Dataset Generation
        ↓
   Data Cleaning & Validation
        ↓
   Exploratory Data Analysis (EDA)
        ↓
   Statistical / Correlation Analysis
        ↓
   SQL Database & Queries
        ↓
   Power BI Dashboard Design
        ↓
   Insights & Recommendations
        ↓
   GitHub Documentation
```

---

## Data Cleaning

The raw dataset contained intentionally injected missing values (~3–5% in selected columns) to demonstrate cleaning techniques.

**Steps performed:**
1. Loaded and inspected shape, data types, and missing values
2. Checked for duplicate records (0 found)
3. Validated all numeric values against expected ranges
4. Filled missing scores with **median** (robust to outliers)
5. Filled missing Certifications/Internship_Months with **0** (logical default)
6. Standardized categorical text values
7. Converted float columns back to integer where appropriate

**Result:** 605 missing cells resolved → 0 missing (excluding intentional Salary NaN for non-placed students)

---

## Exploratory Data Analysis

19 professional charts were generated covering:

- Overall placement rate (62.0%)
- Placement rate by branch, internship, projects, certifications, backlogs, hackathon participation, placement training, CGPA range, gender
- Salary distribution and statistics
- CGPA vs Salary scatter plot with trend line
- Technical score comparison (placed vs not-placed)
- Correlation heatmap
- Placed vs Not-Placed distribution comparison (9 metrics)
- Salary by branch (box plot)
- CGPA distribution by placement status (KDE)

All charts saved to `reports/figures/`.

---

## SQL Analysis

Created a SQLite database and ran **14 analytical queries** including:

- Total students, placed count, placement percentage
- Average CGPA and salary statistics
- Placement rate by branch, internship status, backlogs
- Top 10 students by composite performance score
- Salary statistics by branch
- Placement rate by CGPA range and project count
- Placed vs Not Placed score comparison
- Cross-tabulation: gender × branch placement rates

SQL concepts demonstrated: `SELECT`, `WHERE`, `GROUP BY`, `ORDER BY`, `COUNT`, `AVG`, `SUM`, `ROUND`, `CAST`, `CASE`, `LIMIT`, aggregate functions, conditional aggregation.

---

## Power BI Dashboard

A professional Power BI dashboard was designed with:

- **5 KPI Cards:** Total Students, Placed Students, Placement Rate, Avg CGPA, Avg Salary
- **8 Visualizations:** Branch performance, internship impact, CGPA range analysis, project analysis, backlog analysis, salary distribution, technical score comparison, CGPA vs salary
- **6 Slicers:** Branch, Gender, Internship, Placement Status, Placement Training, Hackathon
- **6 DAX Measures** for dynamic calculations

Detailed step-by-step instructions: [`powerbi/dashboard_instructions.md`](powerbi/dashboard_instructions.md)

---

## Key Insights

| # | Finding | Key Number |
|---|---------|-----------|
| 1 | CGPA is the strongest predictor of placement | r = +0.50 |
| 2 | Backlogs severely reduce placement chances | 73.8% vs 36.4% |
| 3 | Internship experience strongly associated with placement | 74.3% vs 50.2% |
| 4 | Placement training shows meaningful impact | 67.7% vs 54.8% |
| 5 | Higher CGPA shows clear upward trend in placement rate | 17.3% (<5) → 97.8% (9-10) |
| 6 | Technical scores differ notably between placed and non-placed | 62.3 vs 55.4 |
| 7 | CGPA has moderate positive correlation with salary | r = 0.539 |
| 8 | Gender shows minimal difference in placement rates | 62.7% vs 61.5% |
| 9 | Branch placement rates are relatively uniform | 60.6%–64.0% |
| 10 | Hackathon participation shows slight positive association | 67.5% vs 60.0% |

Full analysis: [`reports/insights.md`](reports/insights.md)

---

## Recommendations

**For Students:**
- Maintain CGPA above 7.0 for significantly better placement chances
- Pursue at least one internship (2-3 months minimum)
- Clear backlogs as early as possible
- Attend placement training programs
- Build 2-3 real projects with documentation

**For Colleges:**
- Focus training resources on students in the 6.0–7.0 CGPA range (highest improvement potential)
- Make internship facilitation a priority
- Offer backlog clearing support programs

**For Placement Coordinators:**
- Use CGPA + internship + backlog status as primary indicators for placement readiness
- Design training programs targeting technical skill gaps

---

## Project Structure

```
student-performance-placement-analytics/
│
├── data/
│   ├── raw/
│   │   └── student_placement_data.csv        # Original synthetic data
│   └── processed/
│       └── student_placement_cleaned.csv      # Cleaned data
│
├── src/
│   ├── generate_dataset.py                    # Dataset generation script
│   ├── data_cleaning.py                       # Data cleaning pipeline
│   ├── eda_analysis.py                        # EDA + statistical analysis
│   └── sql_analysis.py                        # SQLite DB creation + queries
│
├── sql/
│   ├── schema.sql                             # Database schema
│   ├── analysis_queries.sql                   # 14 SQL analysis queries
│   └── student_placement.db                   # SQLite database
│
├── reports/
│   ├── figures/                               # All generated charts (19 PNGs)
│   └── insights.md                            # Key insights + recommendations
│
├── powerbi/
│   └── dashboard_instructions.md              # Step-by-step Power BI guide
│
├── docs/
│   ├── interview_preparation.md               # Interview Q&A guide
│   ├── resume_descriptions.md                 # Resume bullet points
│   ├── project_explanations.md                # 30s / 1min / 2min explanations
│   └── troubleshooting.md                     # Common issues + solutions
│
├── screenshots/                               # Dashboard & chart screenshots
│
├── requirements.txt                           # Python dependencies
├── README.md                                  # This file
├── .gitignore                                 # Git ignore rules
└── LICENSE                                    # MIT License
```

---

## How to Run

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Power BI Desktop (free, for dashboard — optional)

### Step-by-step

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/student-performance-placement-analytics.git
cd student-performance-placement-analytics

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Generate the synthetic dataset
python src/generate_dataset.py

# 4. Clean the data
python src/data_cleaning.py

# 5. Run exploratory data analysis (creates charts in reports/figures/)
python src/eda_analysis.py

# 6. Run SQL analysis (creates SQLite DB + prints query results)
python src/sql_analysis.py
```

For the Power BI dashboard, follow the instructions in [`powerbi/dashboard_instructions.md`](powerbi/dashboard_instructions.md).

---

## Screenshots

<!-- Add your screenshots here after creating the Power BI dashboard -->
<!-- Example: -->
<!-- ![Dashboard Overview](screenshots/dashboard_overview.png) -->
<!-- ![Placement by Branch](screenshots/placement_by_branch.png) -->

*Charts generated by the EDA script can be found in the `reports/figures/` directory.*

---

## Future Improvements

- [ ] Add a logistic regression model to predict placement probability
- [ ] Create an interactive Streamlit/Dash web application
- [ ] Add more demographic and socioeconomic variables
- [ ] Implement time-series analysis across multiple academic years
- [ ] Add a Jupyter notebook with narrative analysis
- [ ] Integrate real (anonymized) placement data with proper ethical review
- [ ] Add automated report generation (PDF export)

---

## Disclaimer

> This project uses a **synthetic (fictional) dataset** that was programmatically generated for educational and portfolio demonstration purposes. The data does **not** represent any real students, educational institution, or organization. All patterns in the data were artificially embedded during generation. Any insights derived should be understood as demonstrations of analytical methodology, **not** as real-world findings.

---

**Built as a portfolio project for Data Analytics learning and interview preparation.**
