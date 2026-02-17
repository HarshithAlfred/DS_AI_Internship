import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler , MinMaxScaler

data = {
    "age": [22, 25, 30, 35, 40, 45, 50],
    "salary": [25000, 32000, 48000, 54000, 62000, 72000, 90000]
}

df = pd.DataFrame(data)
print(df)

plt.figure()
plt.subplot(121)
sns.histplot(data=df,x='salary',kde=True)
plt.title('salary')
plt.subplot(122)
sns.histplot(data=df,x='age',kde=True)
plt.title('Age')
plt.show()

stadscaler= StandardScaler()
df_sclar= pd.DataFrame(stadscaler.fit_transform(df), columns=df.columns)
print(df_sclar)
minmax = MinMaxScaler()
df_minmax= pd.DataFrame(minmax.fit_transform(df), columns=df.columns)
print(df_minmax)


plt.figure()
plt.subplot(121)
sns.histplot(df_sclar['salary'],kde=True)
plt.title('salary')
plt.subplot(122)
sns.histplot(df_minmax['salary'],kde=True)
plt.title('Salary')
plt.show()