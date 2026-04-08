import kagglehub
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
# Download latest version
path = kagglehub.dataset_download("yasserh/wine-quality-dataset")

print("Path to dataset files:", path)
df = pd.read_csv(f"{path}/wineQT.csv")

print(df.head())
df = df.drop('Id', axis=1)
x = df.drop('quality', axis=1)
y = df['quality']

xtrain , xtest , ytrain , ytest = train_test_split(x,y, test_size=0.2 , random_state=42)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

knn_raw = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn_raw.fit(xtrain, ytrain)

y_pred_raw = knn_raw.predict(xtest)
raw_acc = accuracy_score(ytest, y_pred_raw)

print("Accuracy WITHOUT scaling:", raw_acc)

scaler = StandardScaler() 
xtrain_scaled = scaler.fit_transform(xtrain)
xtest_scaled = scaler.transform(xtest)

knn_scaled = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
knn_scaled.fit(xtrain_scaled, ytrain)

y_pred_scaled = knn_scaled.predict(xtest_scaled)
scaled_acc = accuracy_score(ytest, y_pred_scaled)

print("Accuracy WITH scaling:", scaled_acc)