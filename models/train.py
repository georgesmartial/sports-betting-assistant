import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load sample data (replace with real match data)
df = pd.read_csv("data/processed/match_data.csv")

# Assume we have a dataset with columns like:
# team1_strength, team2_strength, venue_advantage, result (0=loss, 1=draw, 2=win)

X = df.drop("result", axis=1)
y = df["result"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, preds))

# Save model
joblib.dump(model, "models/trained/soccer_model.pkl")