import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Download latest version
path = kagglehub.dataset_download("arjunbhasin2013/ccdata")

print("Path to dataset files:", path)
df = pd.read_csv(os.path.join(path, "CC GENERAL.csv"))

print(df.head())


X = df[["PURCHASES", "PURCHASES_FREQUENCY"]]

# Apply K-Means (no scaling)
kmeans = KMeans(n_clusters=3, random_state=0)
y_kmeans = kmeans.fit_predict(X)

# Plot
plt.figure(figsize=(7,5))
plt.scatter(X["PURCHASES"], X["PURCHASES_FREQUENCY"],
            c=y_kmeans, cmap='viridis')

plt.scatter(kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            s=200, c='red', marker='X')

plt.title("K-Means WITHOUT Scaling")
plt.xlabel("PURCHASES")
plt.ylabel("PURCHASES_FREQUENCY")
plt.show()

from sklearn.preprocessing import StandardScaler

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-Means
kmeans_scaled = KMeans(n_clusters=3, random_state=0)
y_kmeans_scaled = kmeans_scaled.fit_predict(X_scaled)

# Plot
plt.figure(figsize=(7,5))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1],
            c=y_kmeans_scaled, cmap='viridis')

plt.scatter(kmeans_scaled.cluster_centers_[:, 0],
            kmeans_scaled.cluster_centers_[:, 1],
            s=200, c='red', marker='X')

plt.title("K-Means WITH Scaling")
plt.xlabel("PURCHASES (scaled)")
plt.ylabel("PURCHASES_FREQUENCY (scaled)")
plt.show()