import pandas as pd
from sklearn.preprocessing import LabelEncoder,OneHotEncoder

df = pd.read_csv('cars.csv')

print(df.info())
print(df.describe())

df['Transmission_encoded'] = LabelEncoder().fit_transform(df['Transmission'])
df_modified = pd.get_dummies(df,columns=['Color'],drop_first=True)
print(df_modified.info())
print(df_modified)