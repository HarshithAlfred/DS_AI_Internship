import kagglehub
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
# Download latest version
path = kagglehub.dataset_download("rakeshrau/social-network-ads")

print("Path to dataset files:", path)
df = pd.read_csv(f"{path}/Social_Network_Ads.csv")

print(df.head())

df = df.drop('User ID', axis=1)
x = df[['Age','EstimatedSalary']]
y = df['Purchased']

scaler= StandardScaler()
xtrain , xtest , ytrain , ytest = train_test_split(x,y)
xtrain_scaled = scaler.fit_transform(xtrain)
xtest_scaled = scaler.transform(xtest)

knn_scaled = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn_scaled.fit(xtrain_scaled, ytrain)

y_pred_scaled = knn_scaled.predict(xtest_scaled)
scaled_acc = accuracy_score(ytest, y_pred_scaled)

print("Accuracy WITH scaling:", scaled_acc)

# Function to plot decision boundary
def plot_decision_boundary(X, y, model, title):
    X1, X2 = X[:, 0], X[:, 1]
    
    x1_min, x1_max = X1.min() - 1, X1.max() + 1
    x2_min, x2_max = X2.min() - 1, X2.max() + 1
    
    xx1, xx2 = np.meshgrid(
        np.arange(x1_min, x1_max, 0.01),
        np.arange(x2_min, x2_max, 0.01)
    )
    
    grid = np.array([xx1.ravel(), xx2.ravel()]).T
    Z = model.predict(grid)
    Z = Z.reshape(xx1.shape)
    
    plt.contourf(xx1, xx2, Z, alpha=0.3)
    plt.scatter(X1, X2, c=y, edgecolor='k')
    plt.title(title)
    plt.xlabel('Age (scaled)')
    plt.ylabel('Estimated Salary (scaled)')
    plt.show()

# Try different K values
for k in [1, 15, 100]:
    knn = KNeighborsClassifier(n_neighbors=k, metric='euclidean')
    knn.fit(xtrain_scaled, ytrain)
    
    y_pred = knn.predict(xtest_scaled)
    acc = accuracy_score(ytest, y_pred)
    
    print(f"K = {k}, Accuracy = {acc:.4f}")
    
    plot_decision_boundary(xtrain_scaled, ytrain, knn, f"K = {k}")