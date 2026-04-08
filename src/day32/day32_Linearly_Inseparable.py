import kagglehub
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC, SVC
from sklearn.metrics import accuracy_score
path = kagglehub.dataset_download("colearninglounge/predicting-pulsar-starintermediate")
datatrain = pd.read_csv(f"{path}/pulsar_data_train.csv")
datatest = pd.read_csv(f"{path}/pulsar_data_test.csv")

print(datatrain.head())
print(datatest.head())
data = datatrain



xtrain = datatrain.drop("target_class", axis=1)
ytrain = datatrain["target_class"]
xtest = datatest.drop("target_class" , axis=1)
xtrain = xtrain.fillna(xtrain.mean())
xtest = xtest.fillna(xtest.mean())
print(xtrain.isna().sum())
print(xtest.isna().sum())
scaler = StandardScaler()

xtrain = scaler.fit_transform(xtrain)
xtest = scaler.transform(xtest)


linear_model = LinearSVC()

linear_model.fit(xtrain, ytrain)

linear_train_acc = linear_model.score(xtrain, ytrain)

print("Linear SVC Train Accuracy:", linear_train_acc)


rbf_model = SVC(kernel='rbf')

rbf_model.fit(xtrain, ytrain)

rbf_train_acc = rbf_model.score(xtrain, ytrain)

print("RBF Kernel Train Accuracy:", rbf_train_acc)
