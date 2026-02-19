import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

np.random.seed(42)

heights = np.random.normal(170,scale=10,size=1000)

income = np.random.exponential(50000,size=1000)

score = 100 - np.random.exponential(scale=10 , size=1000)
score = np.clip(score,0,100)

df = pd.DataFrame({
    "Heights": heights,
    "Incomes": income,
    "Scores": score
})

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(df["Heights"], kde=True, ax=axes[0])
axes[0].set_title("Human Heights (Normal)")

sns.histplot(df["Incomes"], kde=True, ax=axes[1])
axes[1].set_title("Household Incomes (Right-Skewed)")

sns.histplot(df["Scores"], kde=True, ax=axes[2])
axes[2].set_title("Easy Exam Scores (Left-Skewed)")

plt.tight_layout()
plt.show()

for col in df.columns:
    mean = df[col].mean()
    mode = df[col].mode()
    print(f"the mean of {df[col]} is {mean}")
    print(f"the mode of {df[col]} is {mode}")
    print("-" * 30)