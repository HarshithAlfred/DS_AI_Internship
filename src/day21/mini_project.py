import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns 
from scipy.stats import zscore

sns.set_style("whitegrid")
sns.set_palette("Set2")   
plt.rcParams['figure.dpi'] = 100

file_path = r"./UberDataset.csv"

data = pd.read_csv(file_path)


#Revenue=Base Fare+(MILES×Rate per Mile)+(Duration×Hourly Rate)
rate_per_mile = 2.50
hourly_rate = 40
base_fare=50
data['START_DATE'] = pd.to_datetime(data['START_DATE'], format='mixed',errors='coerce')
data['END_DATE'] = pd.to_datetime(data['END_DATE'], format='mixed',errors='coerce')

data = data.dropna(subset=['START_DATE', 'END_DATE'])

data['DURATION'] = (data['END_DATE'] - data['START_DATE']).dt.total_seconds() / 3600
data['REVENUE'] = base_fare + (data['MILES'] * rate_per_mile) + (data['DURATION'] * hourly_rate)

print(data.head())
data['HOUR'] = data['START_DATE'].dt.hour
#Peak hour analysis

peak_hours = data['HOUR'].value_counts().sort_index()
print("Peak Hour:", peak_hours)


hourly_demand = data.groupby('HOUR').size()

plt.figure(figsize=(12,6))
hourly_demand.plot(kind='bar', color=sns.color_palette("viridis", len(hourly_demand)))

plt.title("Ride Demand by Hour (Peak)", fontsize=16, fontweight='bold')
plt.xlabel("Hour of Day", fontsize=12)
plt.ylabel("Number of Rides", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#Revenue Distribution
plt.figure(figsize=(10,6))
plt.hist(data['REVENUE'], bins=20, color="#4C72B0", edgecolor='black')

plt.title("Fare Amount Distribution", fontsize=16, fontweight='bold')
plt.xlabel("Fare", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.tight_layout()
plt.show()
#Skewness
print("Skewness:", data['REVENUE'].skew())

#Revenue by Hour
hourly_revenue = data.groupby('HOUR')['REVENUE'].sum()

plt.figure(figsize=(12,6))
hourly_revenue.plot(kind='bar', color=sns.color_palette("coolwarm", len(hourly_revenue)))

plt.title("Revenue by Hour", fontsize=16, fontweight='bold')
plt.xlabel("Hour", fontsize=12)
plt.ylabel("Total Revenue", fontsize=12)
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#z_score
data['z_score'] = zscore(data['REVENUE'])

expensive_rides = data[data['z_score'] > 3]

print("Number of unusually expensive rides:", len(expensive_rides))

#Sampling hourly mean fare distribution
sample_means = []

for i in range(1000):
    sample = data['REVENUE'].sample(100)
    sample_means.append(sample.mean())

plt.figure(figsize=(10,6))
sns.histplot(sample_means, bins=20, kde=True, color="#55A868")

plt.title("Sampling Distribution of Mean Fares", fontsize=16, fontweight='bold')
plt.xlabel("Mean Fare", fontsize=12)
plt.ylabel("Frequency", fontsize=12)
plt.tight_layout()
plt.show()

#Insights
peak_hour = hourly_demand.idxmax()
max_revenue_hour = hourly_revenue.idxmax()

print("Peak Demand Hour:", peak_hour)
print("Highest Revenue Hour:", max_revenue_hour)
print("Fare Skewness:", data['REVENUE'].skew())

# SQL 

conn = sqlite3.connect('ride_sharing.db')
cursor = conn.cursor()

data.to_sql("trips", conn, if_exists="replace", index=False)

#Peak Hour Revenue
query = """
SELECT hour, SUM(REVENUE) AS total_revenue
FROM trips
GROUP BY hour
ORDER BY total_revenue DESC
"""

peak_revenue = pd.read_sql(query, conn)

print(peak_revenue.head())

#Top Peak Hour
query_top = """
SELECT hour, SUM(REVENUE) AS total_revenue
FROM trips
GROUP BY hour
ORDER BY total_revenue DESC
LIMIT 1
"""

top_hour = pd.read_sql(query_top, conn)

print("Peak Revenue Hour:")
print(top_hour)

conn.close()