import joblib
import numpy as np

def predict_match(team1_stats, team2_stats):
    model = joblib.load("models/trained/soccer_model.pkl")
    features = np.array([team1_stats + team2_stats]).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0]  # 0 = loss, 1 = draw, 2 = win