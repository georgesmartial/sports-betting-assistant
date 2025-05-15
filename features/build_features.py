import pandas as pd
import numpy as np


# Example function to generate features from raw match data
def create_features():
    df = pd.read_csv("data/raw/match_history.csv")
    
    # Dummy features for now
    df['team1_strength'] = np.random.rand(len(df))
    df['team2_strength'] = np.random.rand(len(df))
    df['venue_advantage'] = np.random.choice([0, 1], len(df))

    # Target variable
    df['result'] = np.random.choice([0, 1, 2], len(df))  # 0: loss, 1: draw, 2: win

    df.to_csv("data/processed/match_data.csv", index=False)

create_features()