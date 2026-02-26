import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/csv/predicted_data.csv")
backup = pd.read_csv("data/csv/last_data.csv")

df['residual'] = df['wins'] - df['remaining_wins']