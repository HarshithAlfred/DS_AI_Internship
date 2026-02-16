import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df= pd.read_csv('housing.csv')

plt.figure()
sns.scatterplot(x=df['Sqft'], y=df['Price'])
plt.title("Relationship of Square Footage and Price")
plt.xlabel("Square Footage (Sqft)")
plt.ylabel("Price")
plt.show()

plt.figure()
sns.boxplot(x=df['City'],y=df['Sqft'])
plt.title("Relationship of City and Sqft")
plt.xlabel("City")
plt.ylabel("Sqft")
plt.show()