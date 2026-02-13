import pandas as pd
file = pd.read_csv('customer_orders.csv')
df=pd.DataFrame(file) 
print(df)
print(df.isna().sum())    
df= df.fillna(df.median())
df = df.drop_duplicates(subset='order_ID')
print(df)

     