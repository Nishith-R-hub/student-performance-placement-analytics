"""
=============================================================
 STUDENT PERFORMANCE & PLACEMENT ANALYTICS
 SQL Analysis Script
=============================================================
 Purpose : Create a SQLite database from the cleaned CSV,
           execute all analysis queries, and print results.
 Input   : data/processed/student_placement_cleaned.csv
 Output  : sql/student_placement.db
 Note    : This dataset is ENTIRELY SYNTHETIC / FICTIONAL.
=============================================================
"""

import os
import sqlite3
import pandas as pd

# -- Paths ---------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed",
                         "student_placement_cleaned.csv")
DB_PATH = os.path.join(BASE_DIR, "sql", "student_placement.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")
QUERIES_PATH = os.path.join(BASE_DIR, "sql", "analysis_queries.sql")


def section(title):
    print(f"\n{'='*60}\n {title}\n{'='*60}")


# ============================================================
# STEP 1 - Create SQLite database and load data
# ============================================================
section("STEP 1 - Create SQLite Database")

# Load the cleaned CSV
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} rows from CSV.")

# Create / overwrite the SQLite DB
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Execute schema
with open(SCHEMA_PATH, "r") as f:
    schema_sql = f.read()
cursor.executescript(schema_sql)
print("Schema created.")

# Insert data using pandas (convenient for bulk insert)
df.to_sql("students", conn, if_exists="append", index=False)
print(f"Inserted {len(df)} rows into 'students' table.")


# ============================================================
# STEP 2 - Run analysis queries
# ============================================================
section("STEP 2 - Running Analysis Queries")

# Read and split queries file
with open(QUERIES_PATH, "r") as f:
    raw_sql = f.read()

# Split by the separator comments (queries separated by blank lines
# after comments ending with a SELECT)
# Simple approach: split by semicolon, filter out empty/comment-only blocks
query_blocks = raw_sql.split(";")

query_num = 0
for block in query_blocks:
    # Skip blocks with no SELECT statement
    stripped = block.strip()
    if "SELECT" not in stripped.upper():
        continue

    query_num += 1

    # Extract the comment title (first line starting with --)
    lines = stripped.split("\n")
    title = f"Query {query_num}"
    for line in lines:
        line = line.strip()
        if line.startswith("-- QUERY"):
            title = line.lstrip("- ").strip()
            break

    # Extract just the SQL (remove comment lines)
    sql_lines = [l for l in lines if not l.strip().startswith("--")]
    clean_sql = "\n".join(sql_lines).strip()

    if not clean_sql:
        continue

    print(f"\n-- {title} --")
    try:
        result = pd.read_sql_query(clean_sql, conn)
        print(result.to_string(index=False))
    except Exception as e:
        print(f"  ERROR: {e}")

# ============================================================
# Done
# ============================================================
conn.close()
print(f"\n{'='*60}")
print(f" SQL analysis complete!")
print(f" Database saved to: {DB_PATH}")
print(f"{'='*60}")
