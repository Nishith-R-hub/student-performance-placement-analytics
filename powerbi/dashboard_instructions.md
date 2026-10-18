# Student Performance & Placement Analytics: Power BI Dashboard Guide

Welcome to the Power BI guide for the **Student Performance & Placement Analytics** project! This comprehensive, step-by-step guide is designed for beginners. If you've never used Power BI before, don't worry—just follow these steps carefully, and you'll build an impressive, portfolio-ready dashboard.

**Data Source:** `data/processed/student_placement_cleaned.csv`

---

## 1. Getting Started & Creating Calculated Columns

Before building visuals, we need to create a few calculated columns to group our data better.

Go to the **Data view** (the table icon on the left panel), select the `students` table, and click **New Column** from the top ribbon for each of the following:

### A. CGPA Range
```dax
CGPA_Range = SWITCH(TRUE(), 
    students[CGPA]<5, "Below 5", 
    students[CGPA]<6, "5-6", 
    students[CGPA]<7, "6-7", 
    students[CGPA]<8, "7-8", 
    students[CGPA]<9, "8-9", 
    "9-10"
)
```
*Why?* Grouping CGPA makes it easier to visualize trends rather than dealing with hundreds of unique decimal values.

### B. Backlog Status
```dax
Has_Backlogs = IF(students[Backlogs]>0, "Has Backlogs", "No Backlogs")
```
*Why?* This simplifies our analysis by looking at whether a student has *any* backlogs rather than the exact count.

---

## 2. DAX Measures

DAX (Data Analysis Expressions) is Power BI's formula language. Measures calculate results on the fly based on user filters. 

Click **New Measure** on the top ribbon for each of these:

**1. Total Students**
```dax
Total Students = COUNTROWS(students)
```
*Explanation:* `COUNTROWS` simply counts the total number of rows in the `students` table. Each row represents one student.

**2. Placed Students**
```dax
Placed Students = CALCULATE(COUNTROWS(students), students[Placement_Status]="Placed")
```
*Explanation:* `CALCULATE` modifies the context. It counts the rows *only* where the `Placement_Status` column equals "Placed".

**3. Not Placed Students**
```dax
Not Placed Students = CALCULATE(COUNTROWS(students), students[Placement_Status]="Not Placed")
```
*Explanation:* Same as above, but counts students whose status is "Not Placed".

**4. Placement Rate**
```dax
Placement Rate = DIVIDE([Placed Students], [Total Students], 0)
```
*Explanation:* `DIVIDE` safely divides Placed Students by Total Students. The `0` at the end prevents errors if the denominator is zero. *(Note: Format this measure as a Percentage from the formatting ribbon).*

**5. Average CGPA**
```dax
Average CGPA = AVERAGE(students[CGPA])
```
*Explanation:* Calculates the standard average of the CGPA column.

**6. Average Salary**
```dax
Average Salary = CALCULATE(AVERAGE(students[Salary_LPA]), students[Placement_Status]="Placed")
```
*Explanation:* Calculates the average of `Salary_LPA`, but only for students who are actually placed (ignoring zeros/blanks for non-placed students).

---

## 3. Dashboard Layout & Design Setup

A professional layout makes your portfolio stand out.

- **Page Size:** Default 16:9 (1280 x 720).
- **Theme:** We recommend a clean professional theme. Go to **View > Themes** and select a "Classic" or "Executive" theme.
- **Canvas Structure:**
  - **Top Row (Header & KPIs):** Dashboard title and 5-6 KPI Cards.
  - **Right Panel (Slicers):** A vertical strip holding all interactive filters.
  - **Middle Section (Main Visuals):** 2 to 3 larger charts (e.g., Branch, CGPA analysis).
  - **Bottom Section (Secondary Visuals):** 2 to 3 smaller charts (e.g., Backlogs, Internships).

---

## 4. Step-by-Step Visualizations

### 1. KPI Cards
- **Chart Type:** Card
- **Fields:** Create separate cards for `Total Students`, `Placed Students`, `Placement Rate`, `Average CGPA`, and `Average Salary`.
- **Formatting:** Turn off the background, add a subtle border/shadow, and reduce the data label font size to ~24pt.

### 2. Placement Rate by Branch
- **Chart Type:** Clustered Bar Chart
- **Y-Axis:** `Branch`
- **X-Axis:** `Placement Rate` (Measure)
- **Formatting:** Sort descending by Placement Rate. Add data labels.

### 3. Placement Rate by Internship
- **Chart Type:** Clustered Column Chart
- **X-Axis:** `Internship`
- **Y-Axis:** `Placement Rate`
- **Formatting:** Compare Yes vs. No visually.

### 4. Placement Rate by CGPA Range
- **Chart Type:** Line Chart or Clustered Column Chart
- **X-Axis:** `CGPA_Range` (Make sure they are sorted in logical order: Below 5, 5-6, 6-7, etc.)
- **Y-Axis:** `Placement Rate`
- **Formatting:** This will clearly show how higher CGPA correlates with placement.

### 5. Placement Rate by Project Count
- **Chart Type:** Clustered Column Chart
- **X-Axis:** `Number_of_Projects`
- **Y-Axis:** `Placement Rate`
- **Formatting:** Turn on data labels.

### 6. Placement Rate by Backlog Status
- **Chart Type:** Donut Chart
- **Legend:** `Has_Backlogs` (Calculated column)
- **Values:** `Placement Rate`
- **Formatting:** Move legend to the bottom center.

### 7. Salary Distribution
- **Chart Type:** Clustered Column Chart
- **X-Axis:** `Salary_LPA` (Power BI might try to sum this; ensure it's binned or treated as a category, or group it into bins like 3-5LPA, 5-7LPA, etc.)
- **Y-Axis:** Count of `Student_ID`
- **Formatting:** Filter this visual to only show `Placement_Status = "Placed"`.

### 8. Technical Score vs Placement
- **Chart Type:** Clustered Bar Chart (Grouped)
- **Y-Axis:** `Placement_Status`
- **X-Axis:** Average of `Technical_Score`
- **Formatting:** Shows if placed students have a higher average tech score.

### 9. CGPA vs Salary (Scatter Plot)
- **Chart Type:** Scatter Chart
- **Values/Details:** `Student_ID`
- **X-Axis:** `CGPA`
- **Y-Axis:** `Salary_LPA`
- **Formatting:** Filter to show only placed students. This reveals if higher CGPA equals higher pay.

---

## 5. Slicers (Interactive Filters)

Add these to your right-side panel to make the dashboard interactive:
- **Chart Type:** Slicer
- **Fields to add (one per slicer):**
  1. `Branch` (Dropdown)
  2. `Gender` (Checkbox)
  3. `Internship` (Checkbox)
  4. `Placement_Status` (Checkbox)
  5. `Placement_Training` (Checkbox)
  6. `Hackathon_Participation` (Checkbox)
- **Formatting:** Set slicer style to "Dropdown" for long lists, or "Tile/Button" for Yes/No fields to look modern.

---

## 6. Formatting Guidelines

Consistency is key for a professional look:
- **Number Formats:** Click on your measures in the Data pane. Set `Total Students` to whole number with commas (`#,##0`). Set `Placement Rate` to Percentage (`0.0%`). Set `Average Salary` to Decimal (`0.00`) and manually add a text box with "LPA" near it.
- **Colors:** 
  - Placed/Positive: Green (`#2ecc71`)
  - Not Placed/Negative: Red (`#e74c3c`)
  - Neutral/Base: Professional Blue (`#3498db`) or Dark Gray.
- **Fonts:** Use `Segoe UI` or `DIN` consistently. Make titles bold (12-14pt) and axis labels standard (9-10pt).
- **Titles:** Ensure every chart has a clear, readable title (e.g., "Placement Rate by Branch" instead of "Placement Rate by Branch and Placement_Status").

---

## 7. Tips for Making it Portfolio-Ready

1. **Alignment:** Use **Format > Align** to ensure your KPI cards and charts are perfectly straight. Sloppy alignment ruins a good dashboard.
2. **Whitespace:** Don't cram visuals together. Leave a few pixels of padding between every chart.
3. **UI/UX:** Add a subtle background color (like light gray `#f5f5f5`) to the page, and give your charts a white background with a slight shadow. It creates depth.
4. **Exporting for GitHub/LinkedIn:** 
   - **Screenshots:** Use the Windows Snipping Tool (`Win + Shift + S`) to take high-quality screenshots of the full screen.
   - **PDF:** Go to **File > Export > Export to PDF** to create a static document of your work to attach to resumes.
   - Include a short GIF of you clicking the slicers to show it is interactive.

Happy Dashboarding!
