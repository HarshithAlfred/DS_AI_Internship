
import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans


path = kagglehub.dataset_download("spscientist/students-performance-in-exams")

print("Dataset path:", path)


df = pd.read_csv(os.path.join(path, "StudentsPerformance.csv"))

print(df.head())

X = df[["math score", "reading score", "writing score"]]



wcss = []

for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

# Plot Elbow Graph
plt.plot(range(1, 11), wcss, marker='o')
plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")
plt.show()



kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X)

df["Cluster"] = clusters



plt.scatter(X["math score"], X["reading score"], c=clusters)

# Plot centroids
centroids = kmeans.cluster_centers_
plt.scatter(centroids[:, 0], centroids[:, 1], s=200, marker='X')

plt.xlabel("Math Score")
plt.ylabel("Reading Score")
plt.title("Student Clusters with Centroids")
plt.show()



print("Centroids (Average Scores):")
print(centroids)