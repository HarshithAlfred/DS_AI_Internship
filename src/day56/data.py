from sklearn.linear_model import LinearRegression
import numpy as np
import joblib

# dummy data
X = np.array([[1], [2], [3], [4]])
y = np.array([100, 200, 300, 400])

model = LinearRegression()
model.fit(X, y)

# save model
joblib.dump(model, "model.pkl")