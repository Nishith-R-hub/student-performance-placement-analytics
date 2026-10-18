"""
=============================================================
 STUDENT PERFORMANCE & PLACEMENT ANALYTICS
 Exploratory Data Analysis (EDA) + Statistical Analysis
=============================================================
 Purpose : Perform comprehensive EDA on the cleaned dataset,
           create professional charts, compute correlations,
           and compare placed vs non-placed students.
 Input   : data/processed/student_placement_cleaned.csv
 Output  : reports/figures/*.png  (all charts)
 Note    : This dataset is ENTIRELY SYNTHETIC / FICTIONAL.
=============================================================
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for saving
import matplotlib.pyplot as plt
import seaborn as sns

# -- Paths ---------------------------------------------------
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_PATH = os.path.join(BASE_DIR, "data", "processed",
                         "student_placement_cleaned.csv")
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# -- Style ---------------------------------------------------
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
COLORS = {"Placed": "#2ecc71", "Not Placed": "#e74c3c"}
PALETTE = [COLORS["Placed"], COLORS["Not Placed"]]
BAR_COLOR = "#3498db"
FIG_SIZE = (10, 6)

# -- Load data ----------------------------------------------
df = pd.read_csv(DATA_PATH)
placed = df[df["Placement_Status"] == "Placed"]
not_placed = df[df["Placement_Status"] == "Not Placed"]


def save(fig, name):
    """Save figure and close."""
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  [OK] Saved: {name}")


def section(title):
    print(f"\n{'='*60}\n {title}\n{'='*60}")


# ============================================================
# 1. OVERALL SUMMARY STATISTICS
# ============================================================
section("1. Overall Summary Statistics")

total = len(df)
total_placed = len(placed)
total_not_placed = len(not_placed)
placement_rate = total_placed / total * 100
avg_cgpa = df["CGPA"].mean()
avg_aptitude = df["Aptitude_Score"].mean()
avg_tech = df["Technical_Score"].mean()
avg_comm = df["Communication_Score"].mean()
avg_salary = placed["Salary_LPA"].mean()

print(f"  Total students       : {total}")
print(f"  Placed               : {total_placed} ({placement_rate:.1f}%)")
print(f"  Not Placed           : {total_not_placed}")
print(f"  Average CGPA         : {avg_cgpa:.2f}")
print(f"  Average Aptitude     : {avg_aptitude:.1f}")
print(f"  Average Technical    : {avg_tech:.1f}")
print(f"  Average Communication: {avg_comm:.1f}")
print(f"  Average Salary (LPA) : {avg_salary:.2f}")


# ============================================================
# 2. PLACEMENT RATE BY BRANCH
# ============================================================
section("2. Placement Rate by Branch")

branch_stats = df.groupby("Branch")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
).sort_values(ascending=False)
print(branch_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=FIG_SIZE)
branch_stats.plot(kind="bar", color=BAR_COLOR, edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Branch", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_xlabel("Branch")
ax.set_ylim(0, 100)
for i, v in enumerate(branch_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=30, ha="right")
save(fig, "01_placement_rate_by_branch.png")

# WHAT: Bar chart showing placement % per engineering branch.
# WHY : Identify which branches have better placement outcomes.
# INSIGHT: Helps colleges allocate training resources.


# ============================================================
# 3. PLACEMENT RATE BY INTERNSHIP STATUS
# ============================================================
section("3. Placement Rate by Internship Status")

intern_stats = df.groupby("Internship")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(intern_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=(7, 5))
intern_stats.plot(kind="bar", color=[COLORS["Not Placed"], COLORS["Placed"]],
                  edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Internship Status", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_xlabel("Has Internship?")
ax.set_ylim(0, 100)
for i, v in enumerate(intern_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
save(fig, "02_placement_rate_by_internship.png")


# ============================================================
# 4. PLACEMENT RATE BY PROJECT COUNT
# ============================================================
section("4. Placement Rate by Number of Projects")

proj_stats = df.groupby("Number_of_Projects")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(proj_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=FIG_SIZE)
proj_stats.plot(kind="bar", color=BAR_COLOR, edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Number of Projects", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_xlabel("Number of Projects")
ax.set_ylim(0, 100)
for i, v in enumerate(proj_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold", fontsize=9)
plt.xticks(rotation=0)
save(fig, "03_placement_rate_by_projects.png")


# ============================================================
# 5. PLACEMENT RATE BY CERTIFICATION COUNT
# ============================================================
section("5. Placement Rate by Certifications")

cert_stats = df.groupby("Certifications")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(cert_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=FIG_SIZE)
cert_stats.plot(kind="bar", color="#9b59b6", edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Number of Certifications", fontsize=16,
             fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_xlabel("Number of Certifications")
ax.set_ylim(0, 100)
for i, v in enumerate(cert_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold", fontsize=9)
plt.xticks(rotation=0)
save(fig, "04_placement_rate_by_certifications.png")


# ============================================================
# 6. PLACEMENT RATE BY BACKLOG STATUS
# ============================================================
section("6. Placement Rate by Backlog Status")

df["Has_Backlogs"] = df["Backlogs"].apply(lambda x: "Has Backlogs" if x > 0
                                           else "No Backlogs")
backlog_stats = df.groupby("Has_Backlogs")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(backlog_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=(7, 5))
backlog_stats.plot(kind="bar", color=[COLORS["Not Placed"], COLORS["Placed"]],
                   edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Backlog Status", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(backlog_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
save(fig, "05_placement_rate_by_backlogs.png")


# ============================================================
# 7. PLACEMENT RATE BY HACKATHON PARTICIPATION
# ============================================================
section("7. Placement Rate by Hackathon Participation")

hack_stats = df.groupby("Hackathon_Participation")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(hack_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=(7, 5))
hack_stats.plot(kind="bar", color=["#e67e22", "#27ae60"], edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Hackathon Participation", fontsize=16,
             fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(hack_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
save(fig, "06_placement_rate_by_hackathon.png")


# ============================================================
# 8. PLACEMENT RATE BY PLACEMENT TRAINING
# ============================================================
section("8. Placement Rate by Placement Training")

train_stats = df.groupby("Placement_Training")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(train_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=(7, 5))
train_stats.plot(kind="bar", color=["#e74c3c", "#2ecc71"], edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Placement Training", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(train_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
save(fig, "07_placement_rate_by_training.png")


# ============================================================
# 9. PLACEMENT RATE BY CGPA RANGE
# ============================================================
section("9. Placement Rate by CGPA Range")

bins = [0, 5, 6, 7, 8, 9, 10]
labels = ["<5", "5-6", "6-7", "7-8", "8-9", "9-10"]
df["CGPA_Range"] = pd.cut(df["CGPA"], bins=bins, labels=labels, right=False)

cgpa_stats = df.groupby("CGPA_Range", observed=False)["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(cgpa_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=FIG_SIZE)
colors_gradient = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#27ae60", "#1abc9c"]
cgpa_stats.plot(kind="bar", color=colors_gradient, edgecolor="white", ax=ax)
ax.set_title("Placement Rate by CGPA Range", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_xlabel("CGPA Range")
ax.set_ylim(0, 100)
for i, v in enumerate(cgpa_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold", fontsize=9)
plt.xticks(rotation=0)
save(fig, "08_placement_rate_by_cgpa_range.png")


# ============================================================
# 10. SALARY DISTRIBUTION (placed students)
# ============================================================
section("10. Salary Distribution")

print(placed["Salary_LPA"].describe().round(2).to_string())

fig, ax = plt.subplots(figsize=FIG_SIZE)
ax.hist(placed["Salary_LPA"], bins=25, color="#3498db", edgecolor="white", alpha=0.85)
ax.axvline(placed["Salary_LPA"].mean(), color="#e74c3c", linestyle="--", linewidth=2,
           label=f'Mean: ₹{placed["Salary_LPA"].mean():.2f} LPA')
ax.axvline(placed["Salary_LPA"].median(), color="#f39c12", linestyle="--", linewidth=2,
           label=f'Median: ₹{placed["Salary_LPA"].median():.2f} LPA')
ax.set_title("Salary Distribution of Placed Students", fontsize=16, fontweight="bold")
ax.set_xlabel("Salary (LPA)")
ax.set_ylabel("Number of Students")
ax.legend(fontsize=11)
save(fig, "09_salary_distribution.png")


# ============================================================
# 11. CGPA vs SALARY (scatter)
# ============================================================
section("11. CGPA vs Salary")

fig, ax = plt.subplots(figsize=FIG_SIZE)
ax.scatter(placed["CGPA"], placed["Salary_LPA"], alpha=0.5, color="#2980b9",
           edgecolors="white", linewidth=0.5, s=40)
# Trend line
z = np.polyfit(placed["CGPA"], placed["Salary_LPA"], 1)
p = np.poly1d(z)
x_line = np.linspace(placed["CGPA"].min(), placed["CGPA"].max(), 100)
ax.plot(x_line, p(x_line), color="#e74c3c", linewidth=2, linestyle="--",
        label=f"Trend (slope={z[0]:.2f})")
ax.set_title("CGPA vs Salary (Placed Students)", fontsize=16, fontweight="bold")
ax.set_xlabel("CGPA")
ax.set_ylabel("Salary (LPA)")
ax.legend()
save(fig, "10_cgpa_vs_salary.png")


# ============================================================
# 12. TECHNICAL SCORE vs PLACEMENT (box plot)
# ============================================================
section("12. Technical Score vs Placement Status")

print(f"  Placed mean tech    : {placed['Technical_Score'].mean():.1f}")
print(f"  Not Placed mean tech: {not_placed['Technical_Score'].mean():.1f}")

fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(x="Placement_Status", y="Technical_Score", data=df,
            palette=COLORS, ax=ax, order=["Not Placed", "Placed"])
ax.set_title("Technical Score by Placement Status", fontsize=16, fontweight="bold")
save(fig, "11_technical_score_vs_placement.png")


# ============================================================
# 13. INTERNSHIP vs PLACEMENT (count plot)
# ============================================================
section("13. Internship vs Placement")

ct = pd.crosstab(df["Internship"], df["Placement_Status"])
print(ct.to_string())

fig, ax = plt.subplots(figsize=(8, 6))
ct.plot(kind="bar", stacked=True, color=[COLORS["Not Placed"], COLORS["Placed"]],
        edgecolor="white", ax=ax)
ax.set_title("Internship vs Placement Status", fontsize=16, fontweight="bold")
ax.set_ylabel("Number of Students")
ax.set_xlabel("Internship")
plt.xticks(rotation=0)
ax.legend(title="Placement Status")
save(fig, "12_internship_vs_placement.png")


# ============================================================
# 14. PROJECTS vs PLACEMENT (grouped bar)
# ============================================================
section("14. Projects vs Placement")

fig, ax = plt.subplots(figsize=FIG_SIZE)
proj_cross = pd.crosstab(df["Number_of_Projects"], df["Placement_Status"],
                          normalize="index") * 100
proj_cross[["Not Placed", "Placed"]].plot(kind="bar", stacked=True,
    color=[COLORS["Not Placed"], COLORS["Placed"]], edgecolor="white", ax=ax)
ax.set_title("Placement Outcome by Number of Projects", fontsize=16,
             fontweight="bold")
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Number of Projects")
ax.legend(title="Status")
plt.xticks(rotation=0)
save(fig, "13_projects_vs_placement.png")


# ============================================================
# 15. PLACEMENT STATUS PIE CHART
# ============================================================
section("15. Overall Placement Status")

fig, ax = plt.subplots(figsize=(7, 7))
counts = df["Placement_Status"].value_counts()
ax.pie(counts, labels=counts.index, autopct="%1.1f%%",
       colors=[COLORS["Placed"], COLORS["Not Placed"]],
       startangle=90, textprops={"fontsize": 13},
       wedgeprops={"edgecolor": "white", "linewidth": 2})
ax.set_title("Overall Placement Status", fontsize=16, fontweight="bold")
save(fig, "14_placement_status_pie.png")


# ============================================================
# 16. GENDER vs PLACEMENT
# ============================================================
section("16. Placement Rate by Gender")

gender_stats = df.groupby("Gender")["Placement_Status"].apply(
    lambda x: (x == "Placed").mean() * 100
)
print(gender_stats.round(1).to_string())

fig, ax = plt.subplots(figsize=(7, 5))
gender_stats.plot(kind="bar", color=["#3498db", "#e91e63"], edgecolor="white", ax=ax)
ax.set_title("Placement Rate by Gender", fontsize=16, fontweight="bold")
ax.set_ylabel("Placement Rate (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(gender_stats):
    ax.text(i, v + 1.5, f"{v:.1f}%", ha="center", fontweight="bold")
plt.xticks(rotation=0)
save(fig, "15_placement_rate_by_gender.png")


# ============================================================
# 17. HEATMAP - Correlation Matrix
# ============================================================
section("17. Correlation Analysis")

# Create numeric placement column for correlation
df["Placed_Binary"] = (df["Placement_Status"] == "Placed").astype(int)
df["Internship_Binary"] = (df["Internship"] == "Yes").astype(int)

corr_cols = ["CGPA", "Attendance_Percentage", "Aptitude_Score", "Technical_Score",
             "Communication_Score", "Number_of_Projects", "Certifications",
             "Internship_Binary", "Backlogs", "Resume_Score", "Placed_Binary"]
corr_matrix = df[corr_cols].corr().round(2)

print("\nCorrelation with Placement (Placed_Binary):")
print(corr_matrix["Placed_Binary"].sort_values(ascending=False).to_string())

fig, ax = plt.subplots(figsize=(12, 9))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap="RdYlGn", center=0,
            fmt=".2f", linewidths=0.5, ax=ax, vmin=-1, vmax=1,
            annot_kws={"fontsize": 9})
ax.set_title("Correlation Heatmap", fontsize=16, fontweight="bold")
save(fig, "16_correlation_heatmap.png")


# ============================================================
# 18. PLACED vs NOT-PLACED - Comparison
# ============================================================
section("18. Placed vs Not Placed - Detailed Comparison")

compare_cols = ["CGPA", "Aptitude_Score", "Technical_Score",
                "Communication_Score", "Resume_Score", "Attendance_Percentage",
                "Number_of_Projects", "Certifications", "Backlogs"]

comparison = pd.DataFrame({
    "Placed Mean": placed[compare_cols].mean().round(2),
    "Not Placed Mean": not_placed[compare_cols].mean().round(2),
    "Difference": (placed[compare_cols].mean() - not_placed[compare_cols].mean()).round(2)
})
print(comparison.to_string())

fig, axes = plt.subplots(3, 3, figsize=(16, 14))
axes = axes.flatten()

for i, col in enumerate(compare_cols):
    ax = axes[i]
    data_p = placed[col]
    data_np = not_placed[col]
    ax.hist(data_p, bins=20, alpha=0.6, color=COLORS["Placed"], label="Placed",
            edgecolor="white")
    ax.hist(data_np, bins=20, alpha=0.6, color=COLORS["Not Placed"],
            label="Not Placed", edgecolor="white")
    ax.set_title(col, fontsize=12, fontweight="bold")
    ax.legend(fontsize=8)

plt.suptitle("Placed vs Not Placed - Distribution Comparison", fontsize=18,
             fontweight="bold", y=1.01)
plt.tight_layout()
save(fig, "17_placed_vs_not_placed_distributions.png")


# ============================================================
# 19. SALARY BY BRANCH (box plot)
# ============================================================
section("19. Salary by Branch")

salary_by_branch = placed.groupby("Branch")["Salary_LPA"].agg(["mean", "median"]).round(2)
print(salary_by_branch.to_string())

fig, ax = plt.subplots(figsize=FIG_SIZE)
sns.boxplot(x="Branch", y="Salary_LPA", data=placed, palette="viridis", ax=ax)
ax.set_title("Salary Distribution by Branch (Placed Students)", fontsize=16,
             fontweight="bold")
ax.set_ylabel("Salary (LPA)")
plt.xticks(rotation=30, ha="right")
save(fig, "18_salary_by_branch.png")


# ============================================================
# 20. CGPA DISTRIBUTION by Placement Status
# ============================================================
section("20. CGPA Distribution by Placement Status")

fig, ax = plt.subplots(figsize=FIG_SIZE)
sns.kdeplot(placed["CGPA"], fill=True, color=COLORS["Placed"], alpha=0.5,
            label="Placed", ax=ax)
sns.kdeplot(not_placed["CGPA"], fill=True, color=COLORS["Not Placed"], alpha=0.5,
            label="Not Placed", ax=ax)
ax.set_title("CGPA Distribution by Placement Status", fontsize=16, fontweight="bold")
ax.set_xlabel("CGPA")
ax.legend()
save(fig, "19_cgpa_distribution_by_status.png")


# ============================================================
#  STATISTICAL ANALYSIS SUMMARY
# ============================================================
section("STATISTICAL ANALYSIS SUMMARY")

print("\n-- Key Correlations with Placement --")
placement_corr = corr_matrix["Placed_Binary"].drop("Placed_Binary").sort_values(
    ascending=False)
for feat, val in placement_corr.items():
    strength = "Strong" if abs(val) > 0.4 else "Moderate" if abs(val) > 0.2 else "Weak"
    direction = "positive" if val > 0 else "negative"
    print(f"  {feat:30s} r = {val:+.2f}  ({strength} {direction})")

print("\n-- CGPA <-> Salary Correlation (placed only) --")
cgpa_sal_corr = placed["CGPA"].corr(placed["Salary_LPA"])
print(f"  Pearson r = {cgpa_sal_corr:.3f}")

print("\n[!]  IMPORTANT NOTES:")
print("  1. Correlation does NOT prove causation.")
print("  2. This is a synthetic dataset - patterns were embedded")
print("     during generation and reflect modelled assumptions.")
print("  3. Weak correlations do NOT mean a factor is unimportant;")
print("     it may interact with other variables.")
print("  4. Real-world conclusions require real data, controlled")
print("     studies, and domain expertise.")

# Clean up temp columns
df.drop(columns=["Has_Backlogs", "CGPA_Range", "Placed_Binary",
                  "Internship_Binary"], inplace=True, errors="ignore")

print("\n" + "=" * 60)
print(" EDA complete! All charts saved to reports/figures/")
print("=" * 60)
