import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data = { 
"Customer_ID": [1001,1002,1003,1004,1005,1006,1007,1008,1009,1010], 
"Gender": 
["Male","Female","Female","Male","Male","Female","Male","Female","Male","Female"], 
"Age": [25,32,28,45,36,23,40,29,31,27], 
"City_Tier": [1,2,1,3,2,1,3,2,1,2], 
"Avg_Session_Time": [15,10,18,8,12,20,7,16,14,19],  # in minutes 
"Pages_Visited": [5,3,6,2,4,8,2,5,6,7], 
"Products_Viewed": [3,2,4,1,2,5,1,3,4,4], 
"Previous_Purchases": [2,1,3,0,1,4,0,2,3,3], 
"Discount_Used": [1,0,1,0,1,1,0,1,1,1],  # 1=Yes, 0=No 
"Total_Spend": [1200,600,1800,300,900,2500,250,1500,2000,1700] 
} 
df = pd.DataFrame(data)

#Task 1: Univariate Analysis

plt.figure()
sns.histplot(data=df,x='Total_Spend',kde=True)
plt.title('Total_Spend ')
plt.show()

plt.figure()
sns.boxplot(data=df,x='Avg_Session_Time')
plt.title('Avg_Session_Time ')
plt.show()

plt.figure()
sns.barplot(data=df,y='City_Tier')
plt.title('City_Tier distribution  ')
plt.show()

# Task 2: Bivariate Analysis

plt.figure()
plt.scatter(df['Avg_Session_Time'],df['Total_Spend'])
plt.title('Avg_Session_Time vs Total_Spend ')
plt.show()

plt.figure()
plt.scatter(df['Pages_Visited'],df['Total_Spend'])
plt.title('Pages_Visited vs Total_Spend')
plt.show()

plt.figure()
plt.scatter(df['Previous_Purchases'],df['Total_Spend'])
plt.title('Pages_Visited vs Total_Spend')
plt.show()

plt.figure()
sns.boxplot(data=df,x='Discount_Used' ,y='Total_Spend')
plt.title('Discount_Used vs Total_Spend ')
plt.show()

# Task 3: Multivariate Analysis
corr= df.corr(numeric_only=True)
print(corr)


plt.figure()
sns.heatmap(corr,cmap='coolwarm',annot=True)
plt.show()

# Task 4: Subplot Dashboard
plt.figure(figsize=(12,8))
plt.subplot(2,2,1)
plt.scatter(df['Avg_Session_Time'],df['Total_Spend'])
plt.title('Avg_Session_Time vs Total_Spend ')

plt.subplot(2,2,2)
plt.scatter(df['Previous_Purchases'],df['Total_Spend'])
plt.title('Pages_Visited vs Total_Spend')

plt.subplot(2,2,3)
sns.boxplot(data=df,x='Discount_Used' ,y='Total_Spend')
plt.title('Discount_Used vs Total_Spend ')

plt.subplot(2,2,4)
sns.histplot(data=df,x='Total_Spend',kde=True)
plt.tight_layout()
plt.title('Total_Spend ')
plt.show()

