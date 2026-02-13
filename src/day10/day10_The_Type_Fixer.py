import pandas as pd
df = pd.read_csv('sales.csv')

print(df.dtypes)

df['Price'] =df['Price'].str.replace('S','')
df['Date'] =pd.to_datetime(df['Date'])
print(df)
print(df.dtypes)