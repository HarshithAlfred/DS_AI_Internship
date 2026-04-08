# svm_fraud_detection.py
import kagglehub

# Download latest version
path = kagglehub.dataset_download("mlg-ulb/creditcardfraud")

print("Path to dataset files:", path)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report

# 1. Load dataset
df = pd.read_csv(f"{path}/creditcard.csv")

# Features and target
X = df.drop("Class", axis=1)
y = df["Class"]

print("Class distribution:")
print(y.value_counts(normalize=True)) 

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Train standard SVM
svm_standard = SVC(kernel='rbf', random_state=42)
svm_standard.fit(X_train_scaled, y_train)
y_pred_standard = svm_standard.predict(X_test_scaled)

print("\n=== Standard SVM ===")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_standard))
print("\nClassification Report:")
print(classification_report(y_test, y_pred_standard, digits=4))

# 5. Train SVM with class_weight='balanced'
svm_balanced = SVC(kernel='rbf', class_weight='balanced', random_state=42)
svm_balanced.fit(X_train_scaled, y_train)
y_pred_balanced = svm_balanced.predict(X_test_scaled)

print("\n=== Balanced SVM ===")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_balanced))
print("\nClassification Report:")
print(classification_report(y_test, y_pred_balanced, digits=4))

# 6. Key notes:
print("\nNotes:")
print("1. StandardScaler ensures all features contribute equally to SVM distance calculations.")
print("2. class_weight='balanced' forces the SVM to pay more attention to the rare fraud class.")