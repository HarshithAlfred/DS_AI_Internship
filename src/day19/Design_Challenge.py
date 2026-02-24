import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import sqlite3

data = pd.read_csv("manufacturing_quality_dataset.csv")

target_weight = 50
underweight_limit = 47

#1.Are weights normally distributed?

mean = data['Weight'].mean()
median = data['Weight'].median()
std = data['Weight'].std()
skew = data['Weight'].skew()

print("=== NORMAL DISTRIBUTION CHECK ===")
print("Mean:", round(mean,2))
print("Median:", round(median,2))
print("Standard Deviation:", round(std,2))
print("Skewness:", round(skew,2))

if abs(mean - median) < 0.1:
    print("Conclusion: Distribution is approximately NORMAL\n")
else:
    print("Conclusion: Distribution is SKEWED\n")


# Plot histogram with normal curve
sns.set(style='whitegrid')
plt.figure(figsize=(10,6))

sns.histplot(data['Weight'], bins=30, stat='density', alpha=0.5, label='Histogram')

x = np.linspace(data['Weight'].min(), data['Weight'].max(), 100)
normal_curve = norm.pdf(x, mean, std)

plt.plot(x, normal_curve, color='red', linewidth=3, label='Normal Curve')

plt.axvline(mean, color='green', linestyle='-', linewidth=3, label=f'Mean = {mean:.2f}')
plt.axvline(median, color='blue', linestyle='--', linewidth=3, label=f'Median = {median:.2f}')

plt.title("Weight Distribution vs Normal Curve")
plt.xlabel("Weight")
plt.ylabel("Density")
plt.legend()
plt.show()


#2.Are there defective batches?

defective = data[data['Weight'] < underweight_limit]

print("=== DEFECTIVE PART ANALYSIS ===")
print("Total parts:", len(data))
print("Defective parts:", len(defective))

defective_batches = defective['Batch_id'].unique()

print("Number of defective batches:", len(defective_batches))
print("Defective batch IDs:", defective_batches, "\n")


# Batch defect rate
batch_defect_rate = data.groupby('Batch_id')['Weight'].apply(
    lambda x: (x < underweight_limit).mean()
)

print("Top 5 worst batches:")
print(batch_defect_rate.sort_values(ascending=False).head(), "\n")


#3.Probability of underweight product

probability = len(defective) / len(data)

print("=== PROBABILITY ANALYSIS ===")
print("Probability of underweight product:", round(probability,4))
print("Percentage:", round(probability*100,2), "%\n")


# QUESTION 4: Is the process stable? (Control Chart)

UCL = mean + 3*std
LCL = mean - 3*std

print("=== PROCESS STABILITY ANALYSIS ===")
print("Mean:", round(mean,2))
print("Upper Control Limit (UCL):", round(UCL,2))
print("Lower Control Limit (LCL):", round(LCL,2))

out_of_control = data[(data['Weight'] > UCL) | (data['Weight'] < LCL)]

print("Out-of-control parts:", len(out_of_control))

if len(out_of_control) == 0:
    print("Conclusion: Process is STABLE\n")
else:
    print("Conclusion: Process is NOT fully stable\n")


# Control Chart
plt.figure(figsize=(12,6))

plt.plot(data['Weight'], marker='o', linestyle='-', markersize=3)

plt.axhline(mean, color='green', linewidth=2, label='Mean')
plt.axhline(UCL, color='red', linestyle='--', linewidth=2, label='UCL')
plt.axhline(LCL, color='red', linestyle='--', linewidth=2, label='LCL')

plt.title("Process Control Chart")
plt.xlabel("Part Index")
plt.ylabel("Weight")
plt.legend()
plt.show()

#FINAL SUMMARY

print("=== FINAL MANAGEMENT SUMMARY ===")
print("1. Normal Distribution:", "YES" if abs(mean - median) < 0.1 else "NO")
print("2. Defective batches found:", len(defective_batches))
print("3. Underweight probability:", str(round(probability*100,2)) + "%")
print("4. Process stability:", "STABLE" if len(out_of_control) == 0 else "UNSTABLE")

# -----------------------------
# 1. Create Database & Tables
# -----------------------------
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    year INTEGER
)
""")

cursor.execute("""
CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY,
    subject_name TEXT,
    department TEXT
)
""")

cursor.execute("""
CREATE TABLE marks (
    student_id INTEGER,
    subject_id INTEGER,
    marks INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
)
""")

# -----------------------------
# 2. Insert Sample Data
# -----------------------------
students_data = [
    (1, 'Alice', 'Computer Science', 1),
    (2, 'Bob', 'Computer Science', 2),
    (3, 'Charlie', 'Mathematics', 1),
    (4, 'David', 'Mathematics', 2),
    (5, 'Eva', 'Physics', 1),
    (6, 'Frank', 'Physics', 2),
    (7, 'Grace', 'Computer Science', 3),
    (8, 'Helen', 'Mathematics', 3),
    (9, 'Ian', 'Physics', 3),
    (10, 'Jack', 'Computer Science', 4)
]

subjects_data = [
    (101, 'Data Structures', 'Computer Science'),
    (102, 'Algorithms', 'Computer Science'),
    (201, 'Linear Algebra', 'Mathematics'),
    (202, 'Statistics', 'Mathematics'),
    (301, 'Quantum Mechanics', 'Physics'),
    (302, 'Thermodynamics', 'Physics')
]

marks_data = [
    (1, 101, 85),(1, 102, 90),
    (2, 101, 78),(2, 102, 82),
    (3, 201, 88),(3, 202, 92),
    (4, 201, 75),(4, 202, 70),
    (5, 301, 95),(5, 302, 89),
    (6, 301, 60),(6, 302, 65),
    (7, 101, 99),(7, 102, 97),
    (8, 201, 55),(8, 202, 58),
    (9, 301, 72),(9, 302, 68),
    (10,101, 91),(10,102, 94)
]

cursor.executemany("INSERT INTO students VALUES (?,?,?,?)", students_data)
cursor.executemany("INSERT INTO subjects VALUES (?,?,?)", subjects_data)
cursor.executemany("INSERT INTO marks VALUES (?,?,?)", marks_data)

conn.commit()

# -----------------------------
# 3. JOIN Strategy
# -----------------------------
query = """
SELECT s.student_id, s.name, s.department, sub.subject_name, m.marks
FROM students s
JOIN marks m ON s.student_id = m.student_id
JOIN subjects sub ON m.subject_id = sub.subject_id
"""
df = pd.read_sql_query(query, conn)

print("\n--- Joined Data ---")
print(df)

# -----------------------------
# 4. Statistical Calculations
# -----------------------------
mean_marks = df['marks'].mean()
count_marks = df['marks'].count()
variance_marks = df['marks'].var()
std_marks = df['marks'].std()

print("\n--- Overall Statistics ---")
print("Mean:", mean_marks)
print("Count:", count_marks)
print("Variance:", variance_marks)
print("Standard Deviation:", std_marks)

# -----------------------------
# 5. Top 5% Students (by Average)
# -----------------------------
student_avg = df.groupby(['student_id','name'])['marks'].mean().reset_index()
student_avg = student_avg.sort_values(by='marks', ascending=False)

top_5_percent_count = max(1, int(len(student_avg) * 0.05))
top_students = student_avg.head(top_5_percent_count)

print("\n--- Top 5% Students ---")
print(top_students)

# -----------------------------
# 6. Abnormal Performance (Z-score)
# -----------------------------
df['z_score'] = (df['marks'] - mean_marks) / std_marks
outliers = df[np.abs(df['z_score']) > 2]

print("\n--- Abnormal Performance (|Z| > 2) ---")
print(outliers[['student_id','name','marks','z_score']])

# -----------------------------
# 7. Compare Distribution by Department
# -----------------------------
dept_stats = df.groupby('department')['marks'].agg(
    mean='mean',
    count='count',
    variance='var',
    std_dev='std'
).reset_index()

print("\n--- Department Comparison ---")
print(dept_stats)

conn.close()