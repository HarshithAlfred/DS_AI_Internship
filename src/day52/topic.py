from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score, mean_squared_error
from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# fetch dataset
student_performance = fetch_ucirepo(id=320)
print(student_performance)
targets = student_performance.data.targets
X = student_performance.data.features

# Drop unwanted columns (optional)
drop_cols = [
    "guardian", "reason", "nursery",
    "famsize", "Pstatus", "Mjob", "Fjob"
]
X = X.drop(columns=drop_cols, errors="ignore")

# Select useful features based on correlation analysis
selected_features = [
    "higher", "studytime", "Medu", "Fedu",
    "failures", "school", "Dalc", "Walc", "absences", "romantic"
]
# Keep only selected features
X_selected = X[selected_features].copy()

# Add G1 and G2 (important predictors)
X_selected["G1"] = targets["G1"]
X_selected["G2"] = targets["G2"]
y = targets["G3"]

# One-hot encode categorical variables if any remain (should be all numeric now)
X_encoded = pd.get_dummies(X_selected, drop_first=True)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train linear regression model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Predict
y_pred = model.predict(X_test_scaled)

# Metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# For classification-like accuracy (pass/fail threshold = 10)
y_pred_class = (y_pred >= 10).astype(int)
y_test_class = (y_test >= 10).astype(int)
accuracy = accuracy_score(y_test_class, y_pred_class)

print("Accuracy:", accuracy)
print("MSE:", mse)
print("R2 Score:", r2)