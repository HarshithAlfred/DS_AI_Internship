import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
df_h = pd.read_csv('../../data/height.csv')
df_w = pd.read_csv('../../data/weight.csv')


plt.figure()
plt.subplot(121)
sns.histplot(df_h['Height'],kde=True)
plt.title('Height and Weight distribution')
plt.subplot(122)
sns.histplot(df_w['Weight'],kde=True)
plt.tight_layout()
plt.show()

df = pd.merge(df_h,df_w,on='Gender')

# plt.figure()
# plt.subplot(121)
# sns.boxplot(df_h['Height'])
# plt.subplot(122)
# sns.boxplot(df_w['Weight'])
# plt.tight_layout()
# plt.show()
for col in ['Height','Weight']:
 Q1 = df[col].quantile(0.25)
 Q3 = df[col].quantile(0.75)
 IQR =Q3-Q1

 lower_bond = Q1 - 1.5 *IQR
 upper_bond = Q1 + 1.5 *IQR

 outliners = df[(df[col]<lower_bond) | (df[col]>upper_bond)]
 print(F"Outliners for : {col,outliners}")

#task 2

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import zscore
df = pd.read_csv('../../data/bhp.csv')
print(df.head())


lower_bond = df['price_per_sqft'].quantile(0.001)
upper_bond = df['price_per_sqft'].quantile(0.999)

df_modified = df[(df['price_per_sqft']>=lower_bond)&(df['price_per_sqft']<=upper_bond)]
plt.figure()

sns.boxplot(x=df_modified['price_per_sqft'])
plt.show()

#usind 4 Standard deviation 

mean = df_modified['price_per_sqft'].mean()
std = df_modified['price_per_sqft'].std()

lower_bond= mean - 4 * std
upper_bond= mean + 4 * std

df_4std = df_modified[(df_modified['price_per_sqft']>=lower_bond)&(df_modified['price_per_sqft']<=upper_bond)]

plt.figure()

sns.boxplot(x=df_4std['price_per_sqft'])
plt.show()

plt.figure()
sns.histplot(df_4std['price_per_sqft'],kde=True)
plt.tight_layout()
plt.show()

#using the z score

df_modified['Zscore'] = zscore(df_modified['price_per_sqft'])
df_z = df_modified[(df_modified['Zscore'] <= 4) & 
                   (df_modified['Zscore'] >= -4)]
plt.figure()
sns.histplot(df_z['price_per_sqft'],kde=True)
plt.tight_layout()
plt.show()