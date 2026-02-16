import pandas as pd
import numpy as np
df = pd.read_csv(r'..\..\data\students.csv')
#Task 1: Data Cleaning Intelligence

missing_summary_before = df.isnull().sum()

score_columns = ["Math_Score", "Science_Score", "English_Score"]

df[score_columns] = df[score_columns].apply(
    lambda col: col.fillna(col.mean())
)
df["Name"] = df["Name"].str.strip().str.title()
df = df.drop_duplicates(subset="Student_ID")

missing_summary_after = df.isnull().sum()

print("Missing Before:\n", missing_summary_before)
print("Missing After:\n", missing_summary_after)
print("Cleaned Dataset Shape:", df.shape)

print("----------------------------------------------------")
#Task 2: Build a “Risk Score Formula”

#Risk_Score = (Low_Marks * 40) + (Low_Attendance * 30) + (Low_Study * 20) + (Low_Parent_Edu * 10) 
df["Average_Score"] = df[score_columns].mean(axis=1)

df["Low_Marks"] = (df["Average_Score"] < 50).astype(int)
df["Low_Attendance"] = (df["Attendance_Percentage"] < 75).astype(int)
df["Low_Study"] = (df["Study_Hours_per_Week"] < 10).astype(int)
df["Low_Parent_Edu"] = (
    df["Parent_Education_Level"]
    .str.lower()
    .eq("below high school")
).astype(int)

df["Risk_Score"] = (
    df["Low_Marks"] * 40 +
    df["Low_Attendance"] * 30 +
    df["Low_Study"] * 20 +
    df["Low_Parent_Edu"] * 10
)

df["Risk_Level"] = df["Risk_Score"].apply(
    lambda x: "Low Risk" if x <= 30
    else "Medium Risk" if x <= 60
    else "High Risk"
)

print(df[["Student_ID", "Risk_Score", "Risk_Level"]].head())
print("----------------------------------------------------")

#Task 3: Advanced Logical Insights

failures = df[df["Final_Result"] == "Fail"]

subject_failure_means = failures[score_columns].mean().sort_values()

print(subject_failure_means)

low_attendance_students = df[df["Attendance_Percentage"] < 75]

attendance_vs_result = low_attendance_students["Final_Result"].value_counts()

print(attendance_vs_result)

high_risk_passed = df[
    (df["Risk_Level"] == "High Risk") &
    (df["Final_Result"] == "Pass")
]

print(high_risk_passed[["Student_ID", "Risk_Score"]])
avg_study_high_risk = df.loc[
    df["Risk_Level"] == "High Risk",
    "Study_Hours_per_Week"
].mean()

print(f"avg_study_high_risk: {avg_study_high_risk}")

corr_matrix = df[
    score_columns +
    ["Attendance_Percentage", "Study_Hours_per_Week", "Risk_Score"]
].corr()

print(corr_matrix)

print("----------------------------------------------------")

#Task 4: Performance Challenge

import time

start = time.time()

risk_scores_loop = []

for _, row in df.iterrows():
    score = 0
    if row["Average_Score"] < 50:
        score += 40
    if row["Attendance_Percentage"] < 75:
        score += 30
    if row["Study_Hours_per_Week"] < 10:
        score += 20
    if row["Parent_Education_Level"].lower() == "below high school":
        score += 10
    risk_scores_loop.append(score)

df["Risk_Score_Loop"] = risk_scores_loop

loop_time = time.time() - start

start = time.time()

df["Risk_Score_Vectorized"] = (
    (df["Average_Score"] < 50).astype(int) * 40 +
    (df["Attendance_Percentage"] < 75).astype(int) * 30 +
    (df["Study_Hours_per_Week"] < 10).astype(int) * 20 +
    (df["Parent_Education_Level"].str.lower().eq("below high school")).astype(int) * 10
)

vector_time = time.time() - start

print("Loop Time:", loop_time)
print("Vectorized Time:", vector_time)
print("----------------------------------------------------")

#Bonus Level

df["Improvement_Potential"] = (
    (100 - df["Average_Score"]) *
    df["Attendance_Percentage"] / 100
)

high_potential_high_risk = df[
    (df["Improvement_Potential"] > 50) &
    (df["Risk_Level"] == "High Risk")
]

print(high_potential_high_risk[[
    "Student_ID",
    "Improvement_Potential",
    "Risk_Level"
]])
