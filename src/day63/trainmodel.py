"""
===============================================================
  IPL Sports Prediction & Auction Intelligence — TRAINER
===============================================================
  Dataset   : Synthetic IPL player statistics (2008-2024 style)
              Features mimic real Kaggle IPL auction datasets
              (runs, strike rate, avg, wickets, economy, etc.)
  Algorithm : Gradient Boosting Regressor (ensemble of decision
              trees – best accuracy for tabular sports data)
  Target    : Predicted auction sold price (in INR Lakhs)
  Output    : ipl_model.pkl  +  label_encoders.pkl
===============================================================
"""

import numpy as np
import pandas as pd
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.pipeline import Pipeline

# ─────────────────────────────────────────────
# 1. GENERATE REALISTIC IPL PLAYER DATASET
# ─────────────────────────────────────────────
np.random.seed(42)
N = 800   # 800 player auction records

roles        = ["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"]
countries    = ["India", "Australia", "England", "West Indies",
                "South Africa", "New Zealand", "Sri Lanka", "Pakistan"]
base_prices  = [20, 30, 40, 50, 75, 100, 150, 200]   # INR Lakhs

role_arr     = np.random.choice(roles,     N, p=[0.35, 0.30, 0.25, 0.10])
country_arr  = np.random.choice(countries, N, p=[0.50, 0.10, 0.10, 0.08,
                                                   0.08, 0.06, 0.05, 0.03])
base_price_arr = np.random.choice(base_prices, N)
age_arr      = np.random.randint(18, 38, N)
caps_arr     = np.random.randint(0, 150, N)             # international caps
captaincy    = np.random.choice([0, 1], N, p=[0.85, 0.15])

# ── Batting stats (all players have some batting)
runs_arr     = np.where(role_arr == "Bowler",
                         np.random.randint(0, 800, N),
                         np.random.randint(100, 6000, N))
avg_arr      = np.clip(runs_arr / np.maximum(caps_arr, 1) * 1.5 +
                        np.random.normal(0, 5, N), 5, 80)
sr_arr       = np.where(role_arr == "Batsman",
                         np.random.uniform(110, 180, N),
                         np.random.uniform(80, 155, N))
fifties_arr  = np.random.randint(0, 40, N)
hundreds_arr = np.random.randint(0, 10, N)
sixes_arr    = np.random.randint(0, 200, N)
fours_arr    = np.random.randint(0, 400, N)

# ── Bowling stats (bowlers & all-rounders better)
wkts_arr     = np.where(role_arr == "Batsman",
                          np.random.randint(0, 20, N),
                          np.random.randint(5, 200, N))
eco_arr      = np.where(role_arr == "Batsman",
                          np.random.uniform(8, 12, N),
                          np.random.uniform(6, 10, N))
bowl_avg_arr = np.clip(np.random.normal(28, 8, N), 10, 60)
bowl_sr_arr  = np.clip(np.random.normal(22, 6, N), 10, 50)

# ── Target: SOLD PRICE (INR Lakhs) — formula reflects real auction dynamics
sold_price = (
    base_price_arr * 1.2
    + avg_arr      * 8
    + (sr_arr - 100) * 3
    + wkts_arr     * 12
    + (10 - eco_arr) * 20
    + fifties_arr  * 15
    + hundreds_arr * 60
    + sixes_arr    * 2
    + caps_arr     * 3
    + captaincy    * 200
    + (country_arr == "India") * 150
    + np.random.normal(0, 80, N)   # market noise
)
sold_price = np.clip(sold_price, base_price_arr, 2000)  # realistic cap ₹20 Cr

df = pd.DataFrame({
    "PLAYER_ROLE"    : role_arr,
    "COUNTRY"        : country_arr,
    "AGE"            : age_arr,
    "INTERNATIONAL_CAPS": caps_arr,
    "CAPTAINCY_EXP"  : captaincy,
    "BASE_PRICE"     : base_price_arr,
    "RUNS"           : runs_arr,
    "BATTING_AVG"    : avg_arr.round(2),
    "STRIKE_RATE"    : sr_arr.round(2),
    "FIFTIES"        : fifties_arr,
    "HUNDREDS"       : hundreds_arr,
    "SIXES"          : sixes_arr,
    "FOURS"          : fours_arr,
    "WICKETS"        : wkts_arr,
    "ECONOMY_RATE"   : eco_arr.round(2),
    "BOWLING_AVG"    : bowl_avg_arr.round(2),
    "BOWLING_SR"     : bowl_sr_arr.round(2),
    "SOLD_PRICE"     : sold_price.round(0).astype(int)
})

print("=" * 60)
print("  IPL AUCTION PRICE PREDICTION — MODEL TRAINER")
print("=" * 60)
print(f"\n📊 Dataset shape  : {df.shape}")
print(f"   Price range    : ₹{df.SOLD_PRICE.min()} L  –  ₹{df.SOLD_PRICE.max()} L")
print(f"   Mean price     : ₹{df.SOLD_PRICE.mean():.0f} L")
print(f"\n{df.describe().round(1)}")

# ─────────────────────────────────────────────
# 2. PREPROCESSING
# ─────────────────────────────────────────────
label_encoders = {}
for col in ["PLAYER_ROLE", "COUNTRY"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

FEATURES = [c for c in df.columns if c != "SOLD_PRICE"]
X = df[FEATURES]
y = df["SOLD_PRICE"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n📂 Train size: {len(X_train)}  |  Test size: {len(X_test)}")

# ─────────────────────────────────────────────
# 3. MODEL SELECTION — COMPARE ALGORITHMS
# ─────────────────────────────────────────────
print("\n🔍 Comparing algorithms …")

candidates = {
    "RandomForest"       : RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    "GradientBoosting"   : GradientBoostingRegressor(n_estimators=300, learning_rate=0.08,
                                                      max_depth=5, random_state=42),
}

best_name, best_score, best_model = None, -np.inf, None
for name, mdl in candidates.items():
    cv_r2 = cross_val_score(mdl, X_train, y_train, cv=5, scoring="r2").mean()
    print(f"   {name:22s}  →  CV R²: {cv_r2:.4f}")
    if cv_r2 > best_score:
        best_score = cv_r2
        best_name  = name
        best_model = mdl

print(f"\n✅ Best algorithm : {best_name}  (CV R² = {best_score:.4f})")

# ─────────────────────────────────────────────
# 4. HYPERPARAMETER TUNING (GridSearchCV)
# ─────────────────────────────────────────────
print("\n⚙️  Tuning hyperparameters …")

if best_name == "GradientBoosting":
    param_grid = {
        "n_estimators" : [200, 300, 400],
        "learning_rate": [0.05, 0.08, 0.1],
        "max_depth"    : [4, 5, 6],
        "subsample"    : [0.8, 1.0],
    }
    grid = GridSearchCV(
        GradientBoostingRegressor(random_state=42),
        param_grid, cv=5, scoring="r2", n_jobs=-1, verbose=0
    )
else:
    param_grid = {
        "n_estimators"    : [150, 200, 300],
        "max_depth"       : [None, 10, 20],
        "min_samples_split": [2, 5],
    }
    grid = GridSearchCV(
        RandomForestRegressor(random_state=42, n_jobs=-1),
        param_grid, cv=5, scoring="r2", n_jobs=-1, verbose=0
    )

grid.fit(X_train, y_train)
final_model = grid.best_estimator_
print(f"   Best params: {grid.best_params_}")
print(f"   Best CV R² : {grid.best_score_:.4f}")

# ─────────────────────────────────────────────
# 5. FINAL EVALUATION ON TEST SET
# ─────────────────────────────────────────────
y_pred = final_model.predict(X_test)

mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2   = r2_score(y_test, y_pred)

# Accuracy as % within ±25% of actual price
within_25 = np.mean(np.abs(y_pred - y_test) / y_test < 0.25) * 100

print("\n" + "=" * 60)
print("  📈 TEST SET PERFORMANCE")
print("=" * 60)
print(f"   R² Score            : {r2:.4f}   ({r2*100:.1f}%)")
print(f"   MAE                 : ₹{mae:.1f} Lakhs")
print(f"   RMSE                : ₹{rmse:.1f} Lakhs")
print(f"   Accuracy (±25%)     : {within_25:.1f}%")

# Feature importance
fi = pd.Series(final_model.feature_importances_, index=FEATURES)
fi_sorted = fi.sort_values(ascending=False)
print("\n   🔑 Top 10 Feature Importances:")
for feat, imp in fi_sorted.head(10).items():
    bar = "█" * int(imp * 100)
    print(f"   {feat:22s}  {imp:.4f}  {bar}")

# ─────────────────────────────────────────────
# 6. SAVE MODEL & ENCODERS
# ─────────────────────────────────────────────
joblib.dump(final_model,    "ipl_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(FEATURES,       "feature_names.pkl")

print("\n" + "=" * 60)
print("  ✅  SAVED FILES")
print("=" * 60)
print("   📦 ipl_model.pkl         — Trained model")
print("   📦 label_encoders.pkl    — Category encoders")
print("   📦 feature_names.pkl     — Feature list")
print("\n  🏏 Training complete! Run ui_predict.html to use the model.")
print("=" * 60)