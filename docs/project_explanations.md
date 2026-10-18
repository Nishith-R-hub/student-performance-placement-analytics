# Project Explanations

Natural, student-friendly answers for interview settings.

---

## 30-Second Explanation

"For my portfolio project, I built a data analytics project around student placements. I created a synthetic dataset of a thousand students with things like CGPA, internship experience, backlogs, and technical scores, and then I analyzed what factors are most linked to getting placed. I used Python and Pandas for data cleaning and EDA, SQL for structured queries, and Power BI for an interactive dashboard. The main finding was that CGPA is the strongest predictor of placement — students with 8+ CGPA had nearly 90% placement rates — and having backlogs drops placement chances from about 74% down to 36%. It was a really good exercise in the full analytics pipeline."

---

## 1-Minute Explanation

"So for this project, I wanted to understand what factors influence whether engineering students get placed or not. I generated a synthetic dataset of 1,000 students with 21 columns — things like CGPA, branch, technical scores, internship status, certifications, backlogs, and of course the placement outcome and salary.

The first thing I did was data cleaning. I intentionally had some missing values in the raw data, so I handled those using median imputation for scores and zero-fill for things like certifications. Then I did exploratory data analysis — I created about 19 charts looking at placement rates broken down by different factors.

The big findings were: CGPA had the strongest correlation with placement at 0.50, backlogs were really damaging — students without backlogs had a 74% placement rate while those with backlogs had only 36%. Internship experience also made a big difference — 74% placement rate for those with internships versus 50% without.

I also set up a SQLite database and wrote 14 SQL queries for structured analysis, and designed a Power BI dashboard with KPI cards, slicers, and multiple visualizations. Everything is documented on GitHub. It was really useful because it gave me hands-on experience with the entire data analytics workflow — from raw data to business insights."

---

## 2-Minute Explanation

"This project came from a real question I had — what actually matters when it comes to campus placements? So I decided to build a complete data analytics project around it.

I started by creating a synthetic dataset of 1,000 engineering students across six branches — Computer Science, IT, Electronics, Mechanical, Civil, and Electrical. Each student has 21 attributes including CGPA, attendance, aptitude and technical test scores, communication scores, number of projects, certifications, internship experience, backlogs, hackathon participation, and whether they attended placement training. The placement outcome wasn't determined by any single factor — I used a multi-factor probabilistic model with noise, so the data has realistic variation.

For data cleaning, the raw dataset had about 3-5% missing values across six columns. I used median imputation for numeric scores because median is more robust to outliers than mean, and I filled certifications and internship months with zero since missing likely meant 'none.' I also validated all ranges and standardized categorical values.

Then came EDA — this was the bulk of the analytical work. I created 19 charts using Matplotlib and Seaborn. The most important finding was that CGPA had the strongest correlation with placement at r = 0.50. The placement rates by CGPA range tell a clear story: below 5.0 CGPA only 17% got placed, but above 9.0 it was nearly 98%. Backlogs were the second biggest factor — students without backlogs had a 74% placement rate versus 36% with backlogs.

Internship experience was also significant — 74% placement rate with internship versus 50% without. And placement training showed a meaningful difference too, 68% versus 55%.

I also built a SQLite database and ran 14 SQL queries to answer structured questions — placement rates by branch, salary statistics, top performers by composite score, and cross-tabulations of gender and branch. SQL was great for demonstrating how the same analysis can be done in a different paradigm.

For visualization, I designed a Power BI dashboard with five KPI cards, eight chart types, and six slicers for interactive filtering. I wrote custom DAX measures for metrics like placement rate percentage.

The key takeaways were practical: students should focus on maintaining CGPA above 7.0, clear backlogs early, and get at least one internship. Colleges should invest training resources in the 6-7 CGPA range where students have the most to gain. And I was careful to note that correlation doesn't prove causation — these are associations in synthetic data.

The whole project is on GitHub with clean documentation. It gave me real experience with Python, Pandas, SQL, Power BI, and the analytical thinking that goes with data work."
