"""
=============================================================
 STUDENT PERFORMANCE & PLACEMENT ANALYTICS
 Dataset Generation Script
=============================================================
 Purpose : Generate a realistic synthetic dataset of ~1000
           student records with academic, skill, and placement
           information.
 Output  : data/raw/student_placement_data.csv
 Author  : Student Portfolio Project
 Note    : This dataset is ENTIRELY SYNTHETIC / FICTIONAL.
           It does NOT represent any real students or institution.
=============================================================
"""

import os
import numpy as np
import pandas as pd

# -- Fixed seed for reproducibility --------------------------
SEED = 42
np.random.seed(SEED)

# -- Configuration -------------------------------------------
NUM_STUDENTS = 1000

# Branch options and their relative weights
BRANCHES = [
    "Computer Science", "Information Technology",
    "Electronics", "Mechanical", "Civil", "Electrical"
]
BRANCH_WEIGHTS = [0.25, 0.18, 0.15, 0.15, 0.14, 0.13]

# Gender options
GENDERS = ["Male", "Female"]
GENDER_WEIGHTS = [0.58, 0.42]

# Programming language pools per branch family
PROG_SKILLS_CS_IT = ["Python", "Java", "C++", "JavaScript", "C", "Python, Java",
                     "Python, JavaScript", "C++, Java", "C, Python"]
PROG_SKILLS_CORE = ["C", "C++", "MATLAB", "Python", "C, MATLAB", "C++, Python"]

# -- Helper functions ----------------------------------------

def generate_cgpa():
    """
    Generate a realistic CGPA (4.0–10.0 scale) with a right-skewed
    distribution centred around 7.0.
    """
    cgpa = np.random.normal(loc=7.0, scale=1.2, size=NUM_STUDENTS)
    cgpa = np.clip(cgpa, 4.0, 10.0)          # keep within valid range
    return np.round(cgpa, 2)


def generate_attendance():
    """
    Attendance percentage: mostly 60-100 %, with a few low outliers.
    """
    att = np.random.normal(loc=78, scale=10, size=NUM_STUDENTS)
    att = np.clip(att, 40, 100)
    return np.round(att, 1)


def generate_scores(loc, scale, low=0, high=100):
    """Generic score generator with normal distribution."""
    scores = np.random.normal(loc=loc, scale=scale, size=NUM_STUDENTS)
    scores = np.clip(scores, low, high)
    return np.round(scores, 1)


# -- Main generation logic ----------------------------------

def generate_dataset():
    """Build the complete student dataset."""

    # -- Basic demographics ----------------------------------
    student_ids = [f"STU{str(i+1).zfill(4)}" for i in range(NUM_STUDENTS)]
    genders = np.random.choice(GENDERS, NUM_STUDENTS, p=GENDER_WEIGHTS)
    ages = np.random.choice(range(20, 25), NUM_STUDENTS, p=[0.10, 0.30, 0.35, 0.20, 0.05])
    branches = np.random.choice(BRANCHES, NUM_STUDENTS, p=BRANCH_WEIGHTS)
    semesters = np.random.choice([7, 8], NUM_STUDENTS, p=[0.45, 0.55])

    # -- Academic scores -------------------------------------
    cgpa = generate_cgpa()
    attendance = generate_attendance()
    aptitude_score = generate_scores(loc=62, scale=15)
    technical_score = generate_scores(loc=58, scale=16)
    communication_score = generate_scores(loc=60, scale=14)

    # Boost technical scores slightly for CS / IT students
    cs_it_mask = np.isin(branches, ["Computer Science", "Information Technology"])
    technical_score[cs_it_mask] += np.random.uniform(3, 8, cs_it_mask.sum())
    technical_score = np.clip(technical_score, 0, 100).round(1)

    # -- Programming skills ----------------------------------
    programming_skills = []
    for br in branches:
        if br in ["Computer Science", "Information Technology"]:
            programming_skills.append(np.random.choice(PROG_SKILLS_CS_IT))
        else:
            programming_skills.append(np.random.choice(PROG_SKILLS_CORE))

    # -- Projects, certifications, internships ---------------
    num_projects = np.random.choice(
        range(0, 6), NUM_STUDENTS,
        p=[0.08, 0.20, 0.30, 0.25, 0.12, 0.05]
    )
    certifications = np.random.choice(
        range(0, 6), NUM_STUDENTS,
        p=[0.12, 0.25, 0.30, 0.20, 0.10, 0.03]
    )

    # Internship: students with higher CGPA more likely to have one
    internship_prob = 0.25 + (cgpa - 4.0) / (10.0 - 4.0) * 0.45  # 25 %–70 %
    internship = np.array(["Yes" if np.random.random() < p else "No"
                           for p in internship_prob])
    internship_months = np.where(
        internship == "Yes",
        np.random.choice([1, 2, 3, 6], NUM_STUDENTS, p=[0.15, 0.35, 0.30, 0.20]),
        0
    )

    # -- Backlogs --------------------------------------------
    # Lower CGPA -> more likely to have backlogs
    backlog_prob = np.clip(0.7 - (cgpa - 4.0) / 8.0, 0.02, 0.65)
    backlogs = np.array([np.random.choice([0, 1, 2, 3],
                         p=_backlog_dist(p))
                         for p in backlog_prob])

    # -- Other factors ---------------------------------------
    hackathon = np.random.choice(["Yes", "No"], NUM_STUDENTS, p=[0.30, 0.70])
    resume_score = generate_scores(loc=65, scale=12, low=20, high=100)
    placement_training = np.random.choice(["Yes", "No"], NUM_STUDENTS,
                                          p=[0.55, 0.45])

    # -- Placement status (multi-factor probabilistic) -------
    # Build a composite "employability" score then add noise.
    employability = (
        (cgpa - 4.0) / 6.0 * 30           # max 30 pts from CGPA
        + technical_score / 100 * 20        # max 20 pts
        + aptitude_score / 100 * 10         # max 10 pts
        + communication_score / 100 * 10    # max 10 pts
        + (internship == "Yes") * 8         # 8 pts for internship
        + np.minimum(num_projects, 4) * 2   # max 8 pts from projects
        + np.minimum(certifications, 3) * 2 # max 6 pts from certs
        + (hackathon == "Yes") * 3          # 3 pts for hackathon
        + (placement_training == "Yes") * 5 # 5 pts for training
        - backlogs * 6                      # penalty per backlog
    )
    # Add noise so placement is NOT deterministic
    noise = np.random.normal(0, 8, NUM_STUDENTS)
    employability += noise

    # Threshold at ~50th-percentile to get ~60-65 % placement rate
    threshold = np.percentile(employability, 38)
    placement_status = np.where(employability >= threshold, "Placed", "Not Placed")

    # -- Salary (only for placed students) -------------------
    salary = np.zeros(NUM_STUDENTS)
    placed_mask = placement_status == "Placed"
    num_placed = placed_mask.sum()

    base_salary = 3.0 + (cgpa[placed_mask] - 4.0) / 6.0 * 5   # 3–8 base
    tech_bonus  = technical_score[placed_mask] / 100 * 3         # 0–3
    intern_bonus = (internship[placed_mask] == "Yes") * 1.5      # 1.5 if intern
    salary_noise = np.random.normal(0, 1.2, num_placed)

    raw_salary = base_salary + tech_bonus + intern_bonus + salary_noise
    raw_salary = np.clip(raw_salary, 2.5, 18.0)
    salary[placed_mask] = np.round(raw_salary, 2)

    # Not-placed students get NaN salary (realistic)
    salary[~placed_mask] = np.nan

    # -- Assemble DataFrame ----------------------------------
    df = pd.DataFrame({
        "Student_ID": student_ids,
        "Gender": genders,
        "Age": ages,
        "Branch": branches,
        "Semester": semesters,
        "CGPA": cgpa,
        "Attendance_Percentage": attendance,
        "Aptitude_Score": aptitude_score,
        "Technical_Score": technical_score,
        "Communication_Score": communication_score,
        "Programming_Skills": programming_skills,
        "Number_of_Projects": num_projects,
        "Certifications": certifications,
        "Internship": internship,
        "Internship_Months": internship_months,
        "Backlogs": backlogs,
        "Hackathon_Participation": hackathon,
        "Resume_Score": resume_score,
        "Placement_Training": placement_training,
        "Placement_Status": placement_status,
        "Salary_LPA": salary,
    })

    # -- Inject ~3–5 % missing values in selected columns ---
    # This lets us demonstrate data cleaning later
    cols_to_inject = ["Attendance_Percentage", "Aptitude_Score",
                      "Communication_Score", "Resume_Score",
                      "Certifications", "Internship_Months"]
    for col in cols_to_inject:
        mask = np.random.random(NUM_STUDENTS) < 0.04   # ~4 % missing
        df.loc[mask, col] = np.nan

    return df


def _backlog_dist(p):
    """
    Return probability distribution [0, 1, 2, 3] backlogs
    given overall backlog probability *p*.
    """
    no_bl = 1 - p
    return [no_bl, p * 0.55, p * 0.30, p * 0.15]


# -- Entry point ---------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print(" Generating Synthetic Student Dataset")
    print("=" * 60)

    df = generate_dataset()

    # Ensure output directory exists
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "student_placement_data.csv")

    df.to_csv(out_path, index=False)

    # Print summary
    print(f"\n[OK] Dataset saved to: {out_path}")
    print(f"  Rows   : {df.shape[0]}")
    print(f"  Columns: {df.shape[1]}")
    print(f"\n-- Column Info --")
    print(df.dtypes.to_string())
    print(f"\n-- Missing Values --")
    print(df.isnull().sum().to_string())
    print(f"\n-- First 5 Rows --")
    print(df.head().to_string())
    print(f"\n-- Placement Distribution --")
    print(df["Placement_Status"].value_counts().to_string())
    print(f"\n-- Salary Stats (placed students) --")
    print(df["Salary_LPA"].describe().to_string())
    print("\n" + "=" * 60)
    print(" Dataset generation complete!")
    print(" NOTE: This is a SYNTHETIC dataset for educational purposes.")
    print("=" * 60)
