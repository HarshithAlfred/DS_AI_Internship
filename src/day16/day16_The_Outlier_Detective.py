
import pandas as pd
import numpy as np

np.random.seed(42)

heights = np.random.normal(170,scale=10,size=1000)


df = pd.DataFrame({
    "Heights": heights,
})


mean = df['Heights'].mean()
std = df['Heights'].std()
df['zscore'] = (df['Heights'] - mean )  / std

outliners = df[abs(df['zscore']) >3]
print(len(outliners))
