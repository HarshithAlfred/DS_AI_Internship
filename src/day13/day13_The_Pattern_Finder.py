import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df= pd.read_csv('housing.csv')

corr_matrix = df.corr(numeric_only=True)

plt.figure()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

high_corr = corr_matrix.where((corr_matrix>0.8) & (corr_matrix<1.0)).stack().reset_index()
high_corr.columns = ['Var1','Var2','Correlation']
print("Highly correlated pairs (correlation > 0.8):\n", high_corr[high_corr['Correlation'] > 0.8]['Correlation'])

plt.figure()
sns.boxplot(x='City', y='Price', data=df, palette='pastel')
plt.title("Boxplot of Prices by City")
plt.xlabel("City")
plt.ylabel("Price")
plt.show()

Q1 = df['Price'].quantile(0.25)
Q3 = df['Price'].quantile(0.75)
IQR = Q3 - Q1
outliers = df[(df['Price'] < Q1 - 1.5*IQR) | (df['Price'] > Q3 + 1.5*IQR)]
print("Price outliers:\n", outliers)