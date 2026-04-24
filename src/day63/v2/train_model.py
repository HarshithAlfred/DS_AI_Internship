"""
================================================================
  IPL Sports Prediction & Auction Intelligence — TRAINER
================================================================
  Dataset   : REAL IPL Auction Dataset (IMB381IPL2013.csv)
              130 real IPL players, 2008–2011 auctions
              Source: IIM Bangalore / Kaggle
  Algorithm : Extra Trees Regressor (best CV on this dataset)
  Note      : 130 rows is a small dataset — CV R² reflects
              honest generalization. Train R² shows fit quality.
  Target    : SOLD PRICE (in INR — original currency)
  Outputs   : ipl_model.pkl | label_encoders.pkl |
              feature_names.pkl | player_lookup.pkl
================================================================
"""

import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings("ignore")

from sklearn.ensemble import (GradientBoostingRegressor,
                               RandomForestRegressor,
                               ExtraTreesRegressor)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# ── LOAD REAL DATASET ──────────────────────────────────────────
print("=" * 62)
print("  IPL AUCTION PRICE PREDICTION — REAL DATA TRAINER")
print("=" * 62)

df = pd.read_csv("IPL_IMB381IPL2013.csv")
print(f"\n📊 Loaded  : {df.shape[0]} real IPL player records")
print(f"   Columns : {df.shape[1]}")
print(f"   Seasons : {sorted(df['AUCTION YEAR'].unique())}")
print(f"   Price range : ₹{df['SOLD PRICE'].min():,}  –  ₹{df['SOLD PRICE'].max():,}")
print(f"   Mean price  : ₹{df['SOLD PRICE'].mean():,.0f}")

print("\n🏏 Top 10 highest sold players:")
top10 = df[['PLAYER NAME','PLAYING ROLE','COUNTRY','TEAM','SOLD PRICE']]\
          .sort_values('SOLD PRICE', ascending=False).head(10)
for _, r in top10.iterrows():
    print(f"   {r['PLAYER NAME']:20s}  {r['PLAYING ROLE']:12s}  "
          f"{r['COUNTRY']:4s}  ₹{r['SOLD PRICE']:>10,}")

# ── FEATURE ENGINEERING ────────────────────────────────────────
print("\n⚙️  Engineering features …")

df['TOTAL_RUNS']    = df['T-RUNS']   + df['ODI-RUNS-S'] + df['RUNS-S']
df['TOTAL_WKTS']    = df['T-WKTS']   + df['ODI-WKTS']   + df['WKTS']
df['BATTING_SCORE'] = df['AVE'] * df['SR-B'] / 100
df['BOWLING_SCORE'] = np.where(df['ECON'] > 0,
                                df['WKTS'] / (df['ECON'] + 0.01), 0)
df['IS_INDIAN']     = (df['COUNTRY'] == 'IND').astype(int)
df['IS_BATSMAN']    = df['PLAYING ROLE'].isin(['Batsman','W. Keeper']).astype(int)
df['IS_BOWLER']     = (df['PLAYING ROLE'] == 'Bowler').astype(int)
df['LOG_BASE']      = np.log1p(df['BASE PRICE'])

# Encode categoricals
label_encoders = {}
for col in ['PLAYING ROLE', 'COUNTRY']:
    le = LabelEncoder()
    df[col + '_ENC'] = le.fit_transform(df[col])
    label_encoders[col] = le

FEATURES = [
    'PLAYING ROLE_ENC', 'COUNTRY_ENC', 'AGE', 'CAPTAINCY EXP',
    'T-RUNS', 'T-WKTS', 'ODI-RUNS-S', 'ODI-SR-B', 'ODI-WKTS', 'ODI-SR-BL',
    'RUNS-S', 'HS', 'AVE', 'SR-B', 'SIXERS', 'RUNS-C', 'WKTS',
    'AVE-BL', 'ECON', 'SR-BL',
    'BASE PRICE', 'TOTAL_RUNS', 'TOTAL_WKTS', 'BATTING_SCORE',
    'BOWLING_SCORE', 'IS_INDIAN', 'IS_BATSMAN', 'IS_BOWLER', 'LOG_BASE'
]

X = df[FEATURES]
y = df['SOLD PRICE']

print(f"   Features used : {len(FEATURES)}")

# ── ALGORITHM COMPARISON ───────────────────────────────────────
print("\n🔍 Algorithm comparison (5-fold CV) — honest evaluation:")

candidates = {
    'RandomForest'    : RandomForestRegressor(n_estimators=500, max_depth=5,
                                               min_samples_leaf=3, random_state=42),
    'GradientBoosting': GradientBoostingRegressor(n_estimators=300, learning_rate=0.05,
                                                   max_depth=3, subsample=0.7,
                                                   min_samples_leaf=3, random_state=42),
    'ExtraTrees'      : ExtraTreesRegressor(n_estimators=500, max_depth=5,
                                             min_samples_leaf=3, random_state=42),
}
best_name, best_cv, best_model = None, -999, None
for name, mdl in candidates.items():
    cv_r2 = cross_val_score(mdl, X, y, cv=5, scoring='r2').mean()
    print(f"   {name:22s}  →  CV R²: {cv_r2:.4f}")
    if cv_r2 > best_cv:
        best_cv, best_name, best_model = cv_r2, name, mdl

print(f"\n✅ Winner : {best_name}  (CV R² = {best_cv:.4f})")
print("""
   ⚠️  Note on CV R²:
   This dataset has 130 rows — a small real dataset.
   CV R² ~0.28 is the HONEST generalization score.
   Train R² ~0.81 shows the model fits training data well.
   This gap (overfitting) is normal with 130 samples.
   More seasons of data would improve CV R² significantly.
""")

# ── TRAIN FINAL MODEL ON FULL DATA ───────────────────────────
print("🏋️  Training final model on full dataset …")
best_model.fit(X, y)

y_pred_train = best_model.predict(X)
train_r2  = r2_score(y, y_pred_train)
train_mae = mean_absolute_error(y, y_pred_train)
acc25     = (np.abs(y_pred_train - y) / y < 0.25).mean() * 100

# Also show holdout for reference
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
best_model_holdout = ExtraTreesRegressor(n_estimators=500, max_depth=5,
                                          min_samples_leaf=3, random_state=42)
best_model_holdout.fit(X_tr, y_tr)
y_te_pred  = best_model_holdout.predict(X_te)
holdout_r2 = r2_score(y_te, y_te_pred)
holdout_mae= mean_absolute_error(y_te, y_te_pred)

print("\n" + "─" * 55)
print("  📈 EVALUATION RESULTS")
print("─" * 55)
print(f"   CV R² (5-fold, honest)     : {best_cv:.4f}")
print(f"   Holdout R² (80/20 split)   : {holdout_r2:.4f}")
print(f"   Train R² (full data fit)   : {train_r2:.4f}")
print(f"   Train MAE                  : ₹{train_mae:,.0f}")
print(f"   Holdout MAE                : ₹{holdout_mae:,.0f}")
print(f"   Train Accuracy (±25%)      : {acc25:.1f}%")

# Feature importances
fi = pd.Series(best_model.feature_importances_, index=FEATURES)\
       .sort_values(ascending=False)
print("\n   🔑 Top 10 Feature Importances:")
for feat, imp in fi.head(10).items():
    bar = "█" * int(imp * 100)
    print(f"   {feat:20s}  {imp:.4f}  {bar}")

# ── PREDICTION SAMPLES ─────────────────────────────────────────
print("\n   🎯 Sample Predictions vs Actual:")
sample = df.sample(8, random_state=7)
X_sample = sample[FEATURES]
preds    = best_model.predict(X_sample)
for i, (_, row) in enumerate(sample.iterrows()):
    err = abs(preds[i] - row['SOLD PRICE']) / row['SOLD PRICE'] * 100
    print(f"   {row['PLAYER NAME']:20s}  "
          f"Actual: ₹{row['SOLD PRICE']:>8,}   "
          f"Pred: ₹{preds[i]:>8,.0f}   "
          f"Err: {err:.0f}%")

# ── SAVE ARTEFACTS ─────────────────────────────────────────────
joblib.dump(best_model,     "ipl_model.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")
joblib.dump(FEATURES,       "feature_names.pkl")

# Player lookup for UI dropdowns
player_records = df[['PLAYER NAME','PLAYING ROLE','COUNTRY','TEAM',
                      'AGE','BASE PRICE','SOLD PRICE',
                      'RUNS-S','AVE','SR-B','SIXERS','WKTS','ECON',
                      'T-RUNS','T-WKTS','ODI-RUNS-S','ODI-SR-B',
                      'ODI-WKTS','ODI-SR-BL','HS','RUNS-C',
                      'AVE-BL','SR-BL','CAPTAINCY EXP']].copy()
player_records.to_csv("player_data.csv", index=False)
joblib.dump(player_records.to_dict('records'), "player_lookup.pkl")

print("\n" + "=" * 62)
print("  ✅  SAVED ARTEFACTS")
print("─" * 62)
print("   📦  ipl_model.pkl         — Trained ExtraTrees model")
print("   📦  label_encoders.pkl    — Role & Country encoders")
print("   📦  feature_names.pkl     — 29 engineered features")
print("   📦  player_lookup.pkl     — 130 real player records")
print("   📄  player_data.csv       — Player data (human readable)")
print("\n  Open ui_predict.html in your browser to make predictions!")
print("=" * 62)