import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

np.random.seed(42)

income = np.random.exponential(50000,size=1000)

df = pd.DataFrame({
    "Incomes": income
   
})
sns.histplot(df["Incomes"], bins=50, kde=True)
plt.title("Original Distribution (Right-Skewed)")
plt.show()

sample_mean=[]

for _ in range(1000):
    sample = df['Incomes'].sample(n=30,replace=True)
    sample_mean.append(sample.mean())

sns.histplot(sample_mean,bins=30, kde=True)
plt.title("Household Incomes")
plt.show()