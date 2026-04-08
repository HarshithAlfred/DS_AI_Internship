import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np

path = kagglehub.dataset_download("yasserh/wine-quality-dataset")

print("Path to dataset files:", path)
df = pd.read_csv(os.path.join(path, "WineQT.csv"))

# Features & target
X = df.drop("quality", axis=1)
y = df["quality"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

# ✅ Standardize BEFORE PCA
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# PCA (11 → 2)
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

# Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_pca, y_train)

# Accuracy
acc = model.score(X_test_pca, y_test)
print("Accuracy:", acc)
import matplotlib.pyplot as plt

plt.figure(figsize=(8,6))
scatter = plt.scatter(
    X_train_pca[:,0],
    X_train_pca[:,1],
    c=y_train,
    cmap="viridis"
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Projection of Wine Data")
plt.colorbar(scatter, label="Quality")
plt.show()