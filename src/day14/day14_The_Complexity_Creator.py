import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4], [5]])
y = np.array([1, 4, 9, 16, 25])  # y = x^2


poly = PolynomialFeatures(degree=2)

poly_x= poly.fit_transform(X)
model_poly= LinearRegression().fit(poly_x,y)

model_lean = LinearRegression().fit(X,y)

print(f"Linear Regression R2 Score: {int((model_lean.score(X,y))*100)}%")
print(f"Polynomial Features R2 Score: {int((model_poly.score(poly_x,y))*100)}%")
