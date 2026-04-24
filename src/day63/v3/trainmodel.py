# =========================================
# 1. IMPORT LIBRARIES
# =========================================
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from xgboost import XGBClassifier
import joblib

# =========================================
# 2. LOAD DATASET
# =========================================
import kagglehub

path = kagglehub.dataset_download("pratyushpuri/sports-betting-predictive-analysis-dataset")
print("Dataset path:", path)

df = pd.read_csv(f"{path}/sports_betting_predictive_analysis.csv")

print(df.head())
print(df.info())

# =========================================
# 3. DATA CLEANING
# =========================================

# Convert date
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])

# Drop rows with missing odds (IMPORTANT)
df = df.dropna(subset=[
    'Home_Team_Odds',
    'Away_Team_Odds',
    'Draw_Odds'
])

# =========================================
# 4. CREATE TARGET (CRITICAL FIX)
# =========================================
def get_result(row):
    if row['Actual_Winner'] == row['Home_Team']:
        return 'Home'
    elif row['Actual_Winner'] == row['Away_Team']:
        return 'Away'
    else:
        return 'Draw'

df['Result'] = df.apply(get_result, axis=1)

# Encode target
le = LabelEncoder()
df['Result'] = le.fit_transform(df['Result'])

print("\nTarget Mapping:")
print(dict(zip(le.classes_, le.transform(le.classes_))))

# =========================================
# 5. FEATURE ENGINEERING
# =========================================

# Odds features
df['Odds_Diff'] = df['Home_Team_Odds'] - df['Away_Team_Odds']
df['Odds_Ratio'] = df['Home_Team_Odds'] / (df['Away_Team_Odds'] + 1e-5)

# Implied probabilities
df['Home_Prob'] = 1 / df['Home_Team_Odds']
df['Away_Prob'] = 1 / df['Away_Team_Odds']
df['Draw_Prob'] = 1 / df['Draw_Odds']

total_prob = df['Home_Prob'] + df['Away_Prob'] + df['Draw_Prob']
df['Home_Prob'] /= total_prob
df['Away_Prob'] /= total_prob
df['Draw_Prob'] /= total_prob

# Strong feature
df['Favorite'] = (df['Home_Team_Odds'] < df['Away_Team_Odds']).astype(int)

# =========================================
# 6. SELECT FEATURES
# =========================================
features = [
    'Home_Team_Odds',
    'Away_Team_Odds',
    'Draw_Odds',
    'Odds_Diff',
    'Odds_Ratio',
    'Home_Prob',
    'Away_Prob',
    'Draw_Prob',
    'Favorite'
]

X = df[features]
y = df['Result']

# =========================================
# 7. TRAIN TEST SPLIT
# =========================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# =========================================
# 8. SCALING
# =========================================
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# =========================================
# 9. HANDLE CLASS IMBALANCE
# =========================================
class_counts = pd.Series(y_train).value_counts()
weights = y_train.map(lambda x: len(y_train) / class_counts[x])

# =========================================
# 10. TRAIN MODEL
# =========================================
model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    eval_metric='mlogloss',
    random_state=42
)

model.fit(X_train, y_train, sample_weight=weights)

# =========================================
# 11. EVALUATION
# =========================================
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Debug prediction distribution
print("\nPrediction Distribution:")
print(pd.Series(y_pred).value_counts())

# =========================================
# 12. CONFIDENCE + VALUE SCORE
# =========================================
probs = model.predict_proba(X)

df['Confidence'] = np.max(probs, axis=1)

df['Value_Score'] = df['Confidence'] * (
    df['Home_Prob'] + df['Away_Prob']
)

# =========================================
# 13. TOP PICKS
# =========================================
top_values = df.sort_values(by='Value_Score', ascending=False)

print("\n Top Betting Value Picks:")
print(top_values[['Value_Score']].head(10))

# =========================================
# 14. SAVE MODEL
# =========================================
joblib.dump(model, "sports_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le, "label_encoder.pkl")

print("\n Model saved successfully!")