import kagglehub
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
# Download latest version
path = kagglehub.dataset_download("vjchoudhary7/customer-segmentation-tutorial-in-python")

print("Path to dataset files:", path)
df = pd.read_csv(f"{path}/Mall_Customers.csv")
print(df.head())

x = df[["Spending Score (1-100)","Annual Income (k$)"]]
scaler = StandardScaler()

x_scaled = scaler.fit_transform(x)
k_values = [2, 3, 5]

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=0)
    y_kmeans = kmeans.fit_predict(x_scaled)

    plt.figure()
    plt.scatter(x_scaled[:, 0], x_scaled[:, 1], c=y_kmeans, cmap='viridis')
    plt.scatter(kmeans.cluster_centers_[:, 0],
                kmeans.cluster_centers_[:, 1],
                s=200, c='red', marker='X')

    plt.title(f"K-Means Clustering (K={k})")
    plt.xlabel("Spending Score (scaled)")
    plt.ylabel("Estimated Salary (scaled)")
    plt.show()

wcss = []

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(x_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.show()