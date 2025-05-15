import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import os

model_path = "ai_models/predictor.pkl"

def train_model():
    # Simulated historical match data
    data = {
        'home_odds': [1.8, 2.0, 1.6, 2.5, 1.7],
        'away_odds': [2.1, 2.4, 2.8, 1.5, 2.9],
        'result':    [1, 1, 1, 0, 1]  # 1 = home win, 0 = away win
    }
    df = pd.DataFrame(data)

    X = df[['home_odds', 'away_odds']]
    y = df['result']

    model = LogisticRegression()
    model.fit(X, y)

    joblib.dump(model, model_path)
    print("✅ ML model trained and saved.")

def predict_outcome(home_odds, away_odds):
    if not os.path.exists(model_path):
        print("⚠️ Model not trained yet. Run train_model() first.")
        return

    model = joblib.load(model_path)
    prediction = model.predict([[home_odds, away_odds]])[0]

    outcome = "Home Win" if prediction == 1 else "Away Win"
    print(f"🔮 Predicted outcome: {outcome}")