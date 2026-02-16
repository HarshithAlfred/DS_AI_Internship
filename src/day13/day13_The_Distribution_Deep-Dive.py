import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy.stats import skew , kurtosis

df= pd.read_csv('housing.csv')

plt.figure()
sns.histplot(df['Price'],kde=True)
plt.title("Dsitribution of Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

print(f" the Skew value {skew(df['Price'])}")
print(f" the kurtosis value {kurtosis(df['Price'])}")

plt.figure()
sns.countplot(x='City',data=df)
plt.title("Finding the Count of Cities")
plt.xlabel("City")
plt.ylabel("Frequency")
plt.show()