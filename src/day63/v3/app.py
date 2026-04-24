# =========================================
# IMPORTS
# =========================================
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import pandas as pd
import numpy as np
import joblib
import kagglehub

# =========================================
# INIT APP
# =========================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# LOAD MODEL + SCALER + ENCODER
# =========================================
model = joblib.load("sports_model.pkl")
scaler = joblib.load("scaler.pkl")
le = joblib.load("label_encoder.pkl")

# =========================================
# LOAD DATA (for teams dropdown)
# =========================================
path = kagglehub.dataset_download(
    "pratyushpuri/sports-betting-predictive-analysis-dataset"
)
df = pd.read_csv(f"{path}/sports_betting_predictive_analysis.csv")

# =========================================
# INPUT SCHEMA
# =========================================
class MatchInput(BaseModel):
    home_team: str
    away_team: str
    home_odds: float
    away_odds: float
    draw_odds: float

# =========================================
# PREDICTION FUNCTION
# =========================================
def predict_match(data):
    df_input = pd.DataFrame([{
        "Home_Team_Odds": data.home_odds,
        "Away_Team_Odds": data.away_odds,
        "Draw_Odds": data.draw_odds
    }])

    # Feature engineering
    df_input['Odds_Diff'] = df_input['Home_Team_Odds'] - df_input['Away_Team_Odds']
    df_input['Odds_Ratio'] = df_input['Home_Team_Odds'] / (df_input['Away_Team_Odds'] + 1e-5)

    df_input['Home_Prob'] = 1 / df_input['Home_Team_Odds']
    df_input['Away_Prob'] = 1 / df_input['Away_Team_Odds']
    df_input['Draw_Prob'] = 1 / df_input['Draw_Odds']

    total = df_input['Home_Prob'] + df_input['Away_Prob'] + df_input['Draw_Prob']
    df_input['Home_Prob'] /= total
    df_input['Away_Prob'] /= total
    df_input['Draw_Prob'] /= total

    df_input['Favorite'] = (df_input['Home_Team_Odds'] < df_input['Away_Team_Odds']).astype(int)

    features = [
        'Home_Team_Odds','Away_Team_Odds','Draw_Odds',
        'Odds_Diff','Odds_Ratio',
        'Home_Prob','Away_Prob','Draw_Prob','Favorite'
    ]

    X = df_input[features]
    X = scaler.transform(X)

    pred = model.predict(X)[0]
    probs = model.predict_proba(X)[0]

    label = le.inverse_transform([pred])[0]
    confidence = float(np.max(probs))
    value_score = float(confidence * (df_input['Home_Prob'][0] + df_input['Away_Prob'][0]))

    return {
        "prediction": label,
        "confidence": round(confidence, 3),
        "value_score": round(value_score, 3)
    }

# =========================================
# UI PAGE
# =========================================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
    <title>Sports Predictor</title>
    <style>
        body {
            font-family: 'Segoe UI';
            background: linear-gradient(135deg, #141e30, #243b55);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .card {
            background: rgba(255,255,255,0.08);
            padding: 30px;
            border-radius: 15px;
            width: 380px;
            backdrop-filter: blur(12px);
        }

        h2 {
            text-align: center;
        }

        select, input {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            border: none;
        }

        .odds-buttons button {
            margin: 5px;
            padding: 8px 12px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            background: #00c6ff;
            color: white;
        }

        button.main {
            width: 100%;
            padding: 12px;
            background: #00c6ff;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background: #0072ff;
        }

        .result {
            margin-top: 20px;
            font-size: 18px;
            text-align: center;
        }
    </style>
</head>
    <body style="font-family:sans-serif; text-align:center; margin-top:50px; x-scroll:block">
    <div class="card">
        <h2>⚽ Sports Predictor</h2>
        <label>Home Team</label>
        <select id="home"></select>
         <label>Away Team</label>
        <select id="away"></select><br><br>
        <b>Quick Picks:</b><br>

        <label>Home Odds</label>
    <input id="h" type="number" step="0.01">
  
    <div class="odds-buttons">
        
        <button onclick="setOdds('h',1.5)">1.5</button>
        <button onclick="setOdds('h',2.0)">2.0</button>
        <button onclick="setOdds('h',3.0)">3.0</button>
    </div>
    
        <label>Away Odds</label>
    <input id="a" type="number" step="0.01">

    <div class="odds-buttons">
        <button onclick="setOdds('a',1.5)">1.5</button>
        <button onclick="setOdds('a',2.0)">2.0</button>
        <button onclick="setOdds('a',3.0)">3.0</button>
    </div>

        <label>Draw Odds</label>
    <input id="d" type="number" step="0.01">

    <div class="odds-buttons">
        <button onclick="setOdds('d',2.5)">2.5</button>
        <button onclick="setOdds('d',3.0)">3.0</button>
        <button onclick="setOdds('d',4.0)">4.0</button>
    </div>

        <button class="main" onclick="go()">Predict</button>

        <h3 class="result " id="result"></h3>
</div>
        <script>
        function setOdds(id, value) {
    document.getElementById(id).value = value;
}

        async function load() {
            const res = await fetch('/teams');
            const data = await res.json();

            data.teams.forEach(t => {
                home.add(new Option(t,t));
                away.add(new Option(t,t));
            });
        }

        async function go() {
            const data = {
                home_team: home.value,
                away_team: away.value,
                home_odds: parseFloat(h.value),
                away_odds: parseFloat(a.value),
                draw_odds: parseFloat(d.value)
            };

            const res = await fetch('/predict', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body: JSON.stringify(data)
            });

            const r = await res.json();

            document.getElementById("result").innerHTML =
                "🏆 " + r.prediction +
                "<br>📊 Confidence " + r.confidence +
                "<br>💰 ValueScore " + r.value_score;
        }

        load();
        </script>
    </body>
    </html>
    """

# =========================================
# TEAMS API
# =========================================
@app.get("/teams")
def get_teams():
    teams = sorted(set(df["Home_Team"]).union(set(df["Away_Team"])))
    return {"teams": teams}

# =========================================
# PREDICT API
# =========================================
@app.post("/predict")
def predict(input_data: MatchInput):
    return predict_match(input_data)