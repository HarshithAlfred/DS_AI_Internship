import pandas as pd
df = pd.read_csv('city.csv')
df= pd.DataFrame(df)
print(df)
print("Modified data ")
df = df['Location'].str.strip().str.title()
# print(df.columns)

print(df.unique())
print(df)
