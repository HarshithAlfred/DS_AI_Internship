from sklearn.datasets import make_classification
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split , GridSearchCV , RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score , f1_score
import numpy as np
import pandas as pd

# Generate dataset
X, y = make_classification(
    n_samples=1000,    
    n_features=20,  
    weights=[0.9,0.1] ,    
    n_informative=10,    
    n_redundant=5,       
    n_repeated=0,
    n_classes=2,         
    random_state=42
)

# Create feature names (customized for student context)
feature_names = [
    "CGPA", "Internships", "Projects", "Workshops", "Certifications",
    "AptitudeScore", "CodingSkills", "CommunicationSkills", "Backlogs",
    "ExtraCurricular", "Hackathons", "Leadership", "Teamwork",
    "ProblemSolving", "Attendance", "ResearchPapers", "LinkedInActivity",
    "MockInterviewScore", "TechnicalKnowledge", "SoftSkills"
]

df = pd.DataFrame(X, columns=feature_names)
df["Placement"] = y

print(df.head())
xtrain ,xtest, ytrain , ytest = train_test_split(X,y)
scaler = StandardScaler()
x_scaled = scaler.fit_transform(xtrain)
model =RandomForestClassifier()
model.fit(x_scaled,ytrain)
print(model.score(xtest,ytest))

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5, 10]
}
grid_acc = GridSearchCV(
    RandomForestClassifier(random_state=42)
,
 param_grid,
 scoring='accuracy',
 cv=5,
 n_jobs=-1
)

grid_acc.fit(xtrain, ytrain)

print("Best Params (Accuracy):", grid_acc.best_params_)
print("Best Accuracy Score:", grid_acc.best_score_)
grid_f1 = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    scoring='f1',
    cv=5,
    n_jobs=-1
)
import time

start = time.time()
grid_f1.fit(xtrain, ytrain)
grid_time = time.time() - start

print("GridSearch Time:", grid_time)
print("Best Params (F1):", grid_f1.best_params_)
print("Best F1 Score:", grid_f1.best_score_)
param_dist = {
    "n_estimators": np.arange(10, 500),
    "max_depth": [None] + list(np.arange(5, 30)),
    "min_samples_split": np.arange(2, 15)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    scoring='f1',
    cv=5,
    n_jobs=-1,
    random_state=42
)

start = time.time()

random_search.fit(xtrain, ytrain)

random_time = time.time() - start

print("Random Search Time:", random_time)
print("Best F1 (Random):", random_search.best_score_)