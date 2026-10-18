"""
=============================================================
 STUDENT PERFORMANCE & PLACEMENT ANALYTICS
 Data Cleaning Script
=============================================================
 Purpose : Load the raw synthetic dataset, inspect it, handle
           missing values, remove duplicates, validate ranges,
           and save a cleaned version.
 Input   : data/raw/student_placement_data.csv
 Output  : data/processed/student_placement_cleaned.csv
 Note    : This dataset is ENTIRELY SYNTHETIC / FICTIONAL.
=============================================================
"""

import os
import numpy as np
import pandas as pd

# -- Paths ---------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "student_placement_data.csv")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "processed")
CLEAN_PATH = os.path.join(CLEAN_DIR, "student_placement_cleaned.csv")


def section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


# ============================================================
# STEP 1 - Load the raw CSV
# WHY: We need to read the data into a DataFrame before we
#       can inspect or transform anything.
# ============================================================
section("STEP 1 - Load Raw Dataset")
df = pd.read_csv(RAW_PATH)
print(f"Loaded {df.shape[0]} rows x {df.shape[1]} columns from:\n  {RAW_PATH}")


# ============================================================
# STEP 2 - Inspect shape and first rows
# WHY: A quick sanity check ensures the file was read correctly
#       and the columns look as expected.
# ============================================================
section("STEP 2 - Basic Shape Inspection")
print(f"Shape: {df.shape}")
print(f"\nFirst 3 rows:\n{df.head(3).to_string()}")


# ============================================================
# STEP 3 - Data types
# WHY: Knowing data types helps us decide if conversions are
#       needed (e.g., a numeric column stored as object).
# ============================================================
section("STEP 3 - Data Types")
print(df.dtypes.to_string())


# ============================================================
# STEP 4 - Missing values BEFORE cleaning
# WHY: We intentionally injected ~4 % missing values during
#       generation. This step quantifies them so we know what
#       to fix.
# ============================================================
section("STEP 4 - Missing Values (BEFORE cleaning)")
missing_before = df.isnull().sum()
missing_pct = (missing_before / len(df) * 100).round(2)
miss_df = pd.DataFrame({"Missing": missing_before, "Percent": missing_pct})
print(miss_df[miss_df["Missing"] > 0].to_string())
print(f"\nTotal cells missing: {missing_before.sum()}")


# ============================================================
# STEP 5 - Duplicate check
# WHY: Duplicates can skew aggregations and counts.  We check
#       by Student_ID (primary key) and by full-row equality.
# ============================================================
section("STEP 5 - Duplicate Check")
dup_id = df["Student_ID"].duplicated().sum()
dup_row = df.duplicated().sum()
print(f"Duplicate Student_IDs : {dup_id}")
print(f"Duplicate full rows   : {dup_row}")

if dup_row > 0:
    df.drop_duplicates(inplace=True)
    print(f"  -> Removed {dup_row} duplicate rows.")
else:
    print("  -> No duplicates found. No action needed.")


# ============================================================
# STEP 6 - Check invalid / out-of-range values
# WHY: Even synthetic data may have edge cases.  We validate
#       that every column falls within its expected range.
# ============================================================
section("STEP 6 - Range Validation")

range_rules = {
    "CGPA": (4.0, 10.0),
    "Attendance_Percentage": (0, 100),
    "Aptitude_Score": (0, 100),
    "Technical_Score": (0, 100),
    "Communication_Score": (0, 100),
    "Resume_Score": (0, 100),
    "Number_of_Projects": (0, 10),
    "Certifications": (0, 10),
    "Internship_Months": (0, 12),
    "Backlogs": (0, 10),
    "Age": (17, 30),
}

issues_found = 0
for col, (lo, hi) in range_rules.items():
    if col not in df.columns:
        continue
    oob = df[col].dropna()
    bad = ((oob < lo) | (oob > hi)).sum()
    if bad > 0:
        print(f"  [!]  {col}: {bad} values outside [{lo}, {hi}]")
        # Clip to valid range
        df[col] = df[col].clip(lo, hi)
        issues_found += bad

if issues_found == 0:
    print("  [OK] All numeric columns within expected ranges.")
else:
    print(f"  -> Clipped {issues_found} out-of-range values.")


# ============================================================
# STEP 7 - Handle missing values
# WHY: Missing data can break calculations and visualisations.
#       Strategy per column:
#         * Numeric scores -> fill with column MEDIAN
#           (median is more robust to outliers than mean)
#         * Certifications / Internship_Months -> fill with 0
#           (a missing value likely means "none")
# ============================================================
section("STEP 7 - Handle Missing Values")

# Numeric columns -> fill with median
median_fill_cols = ["Attendance_Percentage", "Aptitude_Score",
                    "Communication_Score", "Resume_Score"]
for col in median_fill_cols:
    if df[col].isnull().sum() > 0:
        median_val = df[col].median()
        count = df[col].isnull().sum()
        df[col] = df[col].fillna(median_val)
        print(f"  {col}: filled {count} missing -> median ({median_val})")

# Certifications -> fill with 0
if df["Certifications"].isnull().sum() > 0:
    count = df["Certifications"].isnull().sum()
    df["Certifications"] = df["Certifications"].fillna(0)
    print(f"  Certifications: filled {count} missing -> 0")

# Internship_Months -> fill with 0
if df["Internship_Months"].isnull().sum() > 0:
    count = df["Internship_Months"].isnull().sum()
    df["Internship_Months"] = df["Internship_Months"].fillna(0)
    print(f"  Internship_Months: filled {count} missing -> 0")

# Salary_LPA: NaN for non-placed students is INTENTIONAL - leave it.
print("  Salary_LPA: NaN for 'Not Placed' students kept intentionally.")


# ============================================================
# STEP 8 - Standardise categorical values
# WHY: Inconsistent casing/spelling causes groupby to treat
#       "Yes" and "yes" as different categories.
# ============================================================
section("STEP 8 - Standardise Categorical Values")

cat_cols = ["Gender", "Branch", "Internship", "Hackathon_Participation",
            "Placement_Training", "Placement_Status"]

for col in cat_cols:
    df[col] = df[col].str.strip().str.title()
    print(f"  {col}: {df[col].unique().tolist()}")


# ============================================================
# STEP 9 - Convert data types where necessary
# WHY: Some integer columns may have become float due to NaN.
#       After filling, convert them back to int.
# ============================================================
section("STEP 9 - Data Type Conversion")

int_cols = ["Age", "Semester", "Number_of_Projects", "Certifications",
            "Internship_Months", "Backlogs"]
for col in int_cols:
    df[col] = df[col].astype(int)
    print(f"  {col} -> int")


# ============================================================
# STEP 10 - Final validation
# WHY: Confirm that our cleaning was effective - zero missing
#       values in non-salary columns, correct dtypes, etc.
# ============================================================
section("STEP 10 - Final Validation")

# Missing values AFTER cleaning (excluding Salary_LPA for non-placed)
non_salary = df.drop(columns=["Salary_LPA"])
remaining_missing = non_salary.isnull().sum().sum()
print(f"Missing values (excl. Salary_LPA): {remaining_missing}")

print(f"\nCleaned dataset shape: {df.shape}")
print(f"\nData types:\n{df.dtypes.to_string()}")
print(f"\nPlacement distribution:\n{df['Placement_Status'].value_counts().to_string()}")
print(f"\nCGPA stats:\n{df['CGPA'].describe().to_string()}")


# ============================================================
# STEP 11 - Before / After summary
# ============================================================
section("STEP 11 - Before / After Summary")

# Reload original for comparison
df_original = pd.read_csv(RAW_PATH)
print(f"{'Metric':<35} {'Before':>10} {'After':>10}")
print("-" * 57)
print(f"{'Rows':<35} {df_original.shape[0]:>10} {df.shape[0]:>10}")
print(f"{'Columns':<35} {df_original.shape[1]:>10} {df.shape[1]:>10}")
print(f"{'Total missing cells':<35} {df_original.isnull().sum().sum():>10} "
      f"{df.drop(columns=['Salary_LPA']).isnull().sum().sum():>10}")
print(f"{'Duplicate rows':<35} {df_original.duplicated().sum():>10} "
      f"{df.duplicated().sum():>10}")


# ============================================================
# STEP 12 - Save cleaned dataset
# ============================================================
section("STEP 12 - Save Cleaned Dataset")

os.makedirs(CLEAN_DIR, exist_ok=True)
df.to_csv(CLEAN_PATH, index=False)
print(f"[OK] Cleaned dataset saved to:\n  {CLEAN_PATH}")
print(f"  Rows   : {df.shape[0]}")
print(f"  Columns: {df.shape[1]}")
print("\n" + "=" * 60)
print(" Data cleaning complete!")
print("=" * 60)
