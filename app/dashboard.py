import streamlit as st
import joblib
import numpy as np

st.title("⚽ Sports Betting Assistant")

st.write("Enter team stats to get a match prediction.")

team1_strength = st.slider("Team 1 Strength", 0.0, 1.0, 0.5)
team2_strength = st.slider("Team 2 Strength", 0.0, 1.0, 0.5)
venue_advantage = st.selectbox("Venue Advantage", [0, 1])

if st.button("Predict Outcome"):
    model = joblib.load("../models/trained/soccer_model.pkl")
    features = np.array([[team1_strength, team2_strength, venue_advantage]])
    prediction = model.predict(features)[0]

    if prediction == 0:
        st.error("Prediction: Team 2 Wins")
    elif prediction == 1:
        st.warning("Prediction: Draw")
    else:
        st.success("Prediction: Team 1 Wins")