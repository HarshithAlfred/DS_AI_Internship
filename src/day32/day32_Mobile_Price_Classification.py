import kagglehub
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
path = kagglehub.dataset_download("iabhishekofficial/mobile-price-classification")

datatrain = pd.read_csv(f"{path}/train.csv")
datatest = pd.read_csv(f"{path}/test.csv")

xtrain = datatrain.drop("price_range", axis=1)
ytrain = datatrain["price_range"]  
print(datatrain.head())
print(datatest.head())

xtest = datatest.drop("id", axis=1)  # all input features


C_values = [0.01, 1, 10, 100, 1000 ,10000]
result=[]
for c in C_values:
    model = SVC(C=c)
    model.fit(xtrain,ytrain)
    trainscore = model.score(xtrain,ytrain)
    result.append((c,trainscore))
    
print(result)
