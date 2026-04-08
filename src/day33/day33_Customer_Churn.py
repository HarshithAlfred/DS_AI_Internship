import kagglehub
import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
# Download latest version
path = kagglehub.dataset_download("blastchar/telco-customer-churn")

print("Path to dataset files:", path)

df = pd.read_csv(f"{path}/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Fix TotalCharges
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

# Convert target
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# One-hot encode categorical columns
cat_cols = df.select_dtypes(include=['object']).columns
df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)

print(df_encoded.head())
df_encoded = df_encoded.drop(columns=['customerID'], errors='ignore')

# Features and target
x = df_encoded.drop('Churn', axis=1)
y = df_encoded['Churn']
xtrain , xtest , ytrain , ytest = train_test_split(x,y, test_size=0.2 , random_state=42)

scaler = StandardScaler()
xtrain = scaler.fit_transform(xtrain)
xtest = scaler.transform(xtest)

knn_euclidean = KNeighborsClassifier(n_neighbors=5,metric="euclidean")
knn_euclidean.fit(xtrain,ytrain)
predeuclidean = knn_euclidean.predict(xtest)

knn_manhattan = KNeighborsClassifier(n_neighbors=5,metric="manhattan")
knn_manhattan.fit(xtrain,ytrain)
predmanhattan = knn_manhattan.predict(xtest)

scores1 = []
scores2 =[]
for i in range(1, 16):
    knn_euclidean = KNeighborsClassifier(n_neighbors=5,metric="euclidean")
    knn_euclidean.fit(xtrain,ytrain)
    predeuclidean = knn_euclidean.predict(xtest)

    knn_manhattan = KNeighborsClassifier(n_neighbors=5,metric="manhattan")
    knn_manhattan.fit(xtrain,ytrain)
    predmanhattan = knn_manhattan.predict(xtest)
    scores1.append(accuracy_score(ytest, predeuclidean))
    scores2.append(accuracy_score(ytest, predmanhattan))

# Display the scores for each k
for k, score in enumerate(scores1, 1):
    print(f"k = {k}: {score:.4f}")
for k, score in enumerate(scores2, 1):
    print(f"k = {k}: {score:.4f}")

import matplotlib.pyplot as plt

plt.plot(range(1, 16), scores1)
plt.xlabel("k value")
plt.ylabel("Accuracy")
plt.title("Accuracy vs. k-value for KNN")
plt.show()


plt.plot(range(1, 16), scores2)
plt.xlabel("k value")
plt.ylabel("Accuracy")
plt.title("Accuracy vs. k-value for KNN")
plt.show()

print("Euclidean Accuracy:", accuracy_score(ytest, predeuclidean))
print("Manhattan Accuracy:", accuracy_score(ytest, predmanhattan))