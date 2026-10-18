# Troubleshooting Guide

Common problems and solutions when running this project.

---

## Python Issues

### "Python is not recognized as an internal or external command"

**Cause:** Python is not added to your system PATH.

**Fix:**
1. Open the Python installer again (or download from [python.org](https://python.org))
2. Check the box **"Add Python to PATH"** at the bottom of the installer
3. Click "Modify" or reinstall
4. Restart your terminal/command prompt
5. Verify: `python --version`

### "pip is not recognized"

**Fix:**
```bash
python -m pip install --upgrade pip
```
If that doesn't work, reinstall Python with the "Add to PATH" option checked.

### Package installation fails ("ModuleNotFoundError")

**Fix:**
```bash
pip install -r requirements.txt
```

If you get permission errors:
```bash
pip install --user -r requirements.txt
```

### "No module named 'numpy'" (or pandas, matplotlib, seaborn)

**Fix:**
```bash
pip install numpy pandas matplotlib seaborn
```

Make sure you're using the same Python environment where you installed packages. Check with:
```bash
python -c "import pandas; print(pandas.__version__)"
```

---

## CSV / File Path Issues

### "FileNotFoundError: No such file or directory"

**Cause:** The script can't find the CSV file.

**Fix:**
1. Make sure you run the scripts from the **project root directory**:
   ```bash
   cd student-performance-placement-analytics
   python src/generate_dataset.py
   ```
2. Run `generate_dataset.py` FIRST to create the raw CSV
3. Run `data_cleaning.py` SECOND to create the cleaned CSV
4. Then run `eda_analysis.py` or `sql_analysis.py`

### "UnicodeDecodeError" when reading CSV

**Fix:** Specify encoding when reading:
```python
df = pd.read_csv("file.csv", encoding="utf-8")
# or
df = pd.read_csv("file.csv", encoding="latin-1")
```

### "UnicodeEncodeError" when printing to terminal (Windows)

**Cause:** Windows terminal doesn't support certain Unicode characters.

**Fix:** Set the console encoding:
```bash
chcp 65001
```
Or run Python with UTF-8 mode:
```bash
set PYTHONUTF8=1
python src/eda_analysis.py
```

---

## Pandas Errors

### "ChainedAssignmentError" or "SettingWithCopyWarning"

**Cause:** Newer versions of Pandas (2.0+) use Copy-on-Write.

**Fix:** Instead of:
```python
df["col"].fillna(0, inplace=True)  # OLD way - may not work
```
Use:
```python
df["col"] = df["col"].fillna(0)    # NEW way - always works
```

### "IntCastingNaNError: Cannot convert non-finite values to integer"

**Cause:** Trying to convert a column with NaN values to integer.

**Fix:** Fill NaN first, then convert:
```python
df["col"] = df["col"].fillna(0).astype(int)
```

### "KeyError: column_name"

**Cause:** Column name doesn't exist or has extra spaces.

**Fix:** Check column names:
```python
print(df.columns.tolist())
```

---

## SQL / SQLite Errors

### "sqlite3.OperationalError: no such table: students"

**Cause:** The table hasn't been created yet.

**Fix:** Run `sql_analysis.py` first — it creates the database and table:
```bash
python src/sql_analysis.py
```

### "sqlite3.OperationalError: table students already exists"

**Cause:** Running the schema creation twice.

**Fix:** The schema uses `DROP TABLE IF EXISTS` to handle this. If you still get errors, delete the `.db` file and re-run:
```bash
del sql\student_placement.db
python src/sql_analysis.py
```

### Can't open .db file

SQLite `.db` files are binary — you can't open them in a text editor. Use:
- **DB Browser for SQLite** (free): https://sqlitebrowser.org/
- **Python**: `sqlite3` module (already used in our script)
- **VS Code**: SQLite extension

---

## Power BI Issues

### Can't import CSV file

**Fix:**
1. Open Power BI Desktop
2. Click **Home > Get Data > Text/CSV**
3. Navigate to `data/processed/student_placement_cleaned.csv`
4. Click **Load** (not Transform — we already cleaned the data)

### Columns show wrong data types

**Fix:** In Power BI:
1. Go to **Model view** or **Data view**
2. Click the column header
3. In the **Column tools** tab, change the data type
4. CGPA, Scores, Salary → Decimal Number
5. Student_ID, Gender, Branch → Text
6. Age, Projects, Certifications → Whole Number

### DAX measure shows error

**Common fixes:**
- Check that table name matches (it should be `students` or whatever Power BI named your imported table)
- Make sure column references use square brackets: `students[CGPA]`
- DAX uses commas for function arguments, not semicolons (unless your locale uses semicolons)

### Slicers not filtering correctly

**Fix:**
1. Check that all visuals are on the same page
2. Make sure there are no filters applied at the visual level that override slicers
3. Click on the slicer, then go to **Format > Edit interactions** to verify connections

### Dashboard looks different from instructions

Power BI versions may differ slightly. The core functionality is the same — chart types, DAX, and slicers work the same across versions.

---

## Git / GitHub Issues

### "git is not recognized as an internal or external command"

**Fix:** Install Git from https://git-scm.com/download/win
Restart your terminal after installation.

### "fatal: not a git repository"

**Fix:** Initialize git in your project folder:
```bash
cd student-performance-placement-analytics
git init
```

### "error: failed to push some refs to remote"

**Cause:** Remote has changes you don't have locally.

**Fix:**
```bash
git pull origin main --rebase
git push origin main
```

### "fatal: remote origin already exists"

**Fix:**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/student-performance-placement-analytics.git
```

### Large file warning (>50 MB)

**Cause:** The `.db` file or large charts may exceed GitHub's file size limit.

**Fix:** Add to `.gitignore`:
```
sql/*.db
```
The database can be regenerated by running `sql_analysis.py`.

### Push rejected (authentication)

**Fix:** GitHub no longer accepts passwords. Use a Personal Access Token:
1. Go to GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate a new token with `repo` scope
3. Use the token as your password when pushing

---

## Matplotlib / Chart Issues

### "Matplotlib is currently using agg, which is a non-GUI backend"

This is **not an error** — the script uses `Agg` backend intentionally to save charts without displaying them. Charts are saved to `reports/figures/`.

### Charts look blurry

**Fix:** Increase DPI when saving:
```python
fig.savefig("chart.png", dpi=200, bbox_inches="tight")
```
Our scripts already use `dpi=150`.

### Charts don't show in Jupyter Notebook

Add this to the top of your notebook:
```python
%matplotlib inline
```

---

## General Tips

1. **Always run scripts in order:** generate → clean → eda → sql
2. **Run from the project root directory**, not from inside `src/`
3. **Check Python version:** `python --version` (need 3.8+)
4. **If something breaks**, try deleting generated files and re-running from step 1
5. **Read error messages carefully** — Python error messages usually tell you exactly what's wrong and on which line
