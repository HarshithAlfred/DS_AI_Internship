import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

# Download latest version
path = kagglehub.dataset_download("vjchoudhary7/customer-segmentation-tutorial-in-python")

print("Path to dataset files:", path)
df = pd.read_csv(os.path.join(path, "Mall_Customers.csv"))


print(df.head
      ())
features = ["Age","Annual Income (k$)","Spending Score (1-100)"]

x = df[features]

scaler = StandardScaler()
xscaled = scaler.fit_transform(x)
pca = PCA()
pca.fit(xscaled)

explained_variance = pca.explained_variance_ratio_
print(explained_variance)
cumulative_variance = np.cumsum(explained_variance)

plt.plot(range(1, len(cumulative_variance)+1), cumulative_variance, marker='o')
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("Scree Plot")
plt.grid()
plt.show()