import kagglehub
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
import time
path = kagglehub.dataset_download("datamunge/sign-language-mnist")

print("Dataset path:", path)


dftest = pd.read_csv(os.path.join(path, "sign_mnist_test/sign_mnist_test.csv"))
dftrain = pd.read_csv(os.path.join(path, "sign_mnist_train/sign_mnist_train.csv"))

print(dftest.head
      ())
print(dftrain.head
      ())
xtest= dftest.drop('label',axis=1)
ytest= dftest[["label"]]
xtrain= dftrain.drop('label',axis=1)
ytrain= dftrain[["label"]]

starttime = time.time()
model = LogisticRegression(max_iter=1000)
model.fit(xtrain,ytrain)
endtime = time.time() - starttime 
accuracy = model.score(xtest , ytest)
print(f"Accuracy: {accuracy}")
print(f"run time {endtime}")


pca = PCA (n_components=50)
x_scaledtrain = pca.fit_transform(xtrain)
x_scaledtest = pca.transform(xtest)

starttime = time.time()
model = LogisticRegression(max_iter=1000)
model.fit(x_scaledtrain,ytrain)
lendtime = time.time() - starttime 
accuracy = model.score(x_scaledtest, ytest)
print(f"Accuracy: {accuracy}")
print(f"run time {lendtime}")

print( f" Speed up {endtime/lendtime}X")