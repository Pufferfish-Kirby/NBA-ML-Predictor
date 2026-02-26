import pandas as pd
import numpy as np
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, RidgeCV
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler

train_df = pd.read_csv("data/csv/last_data.csv")
test_df = pd.read_csv("data/csv/summarized_data.csv")

X = train_df.drop(columns=["team_id", "remaining_wins", "Unnamed: 0"])
y_train = train_df["remaining_wins"]
scaler = StandardScaler().set_output(transform="pandas")
X_scaled = scaler.fit_transform(X)

X_tr, X_val, y_tr, y_val = train_test_split(X_scaled, y_train, train_size=0.3, random_state=42)

model = GradientBoostingRegressor(
    n_estimators=400,
    learning_rate=0.02,
    max_depth=5,
    min_samples_leaf=5, 
    subsample=0.8,
    random_state=42
)
model.fit(X_tr, y_tr)
y_pred = model.predict(X_val)
mae = mean_absolute_error(y_val, y_pred) # around 0.1117
y_mean = y_train.mean()
baseline_pred = np.full(len(y_val), y_mean) #full makes the shape of what we want
baseline_mae = mean_absolute_error(y_val, baseline_pred)
print(mae, baseline_mae)

ridge = RidgeCV(alphas=[0.01, 0.1, 0.5, 1, 5, 10, 30, 50, 100])
ridge.fit(X_tr, y_tr)

ridge_preds = ridge.predict(X_val)
ridge_mae = mean_absolute_error(y_val, ridge_preds)
print(ridge_mae)

coefficients = pd.Series(
    ridge.coef_,
    index=X_scaled.columns
).sort_values(ascending=False)

print(coefficients)


X_test = test_df.drop(columns=["team_id", "remaining_wins", "Unnamed: 0"])
X_test_scaled = scaler.transform(X_test)

predicted_remaining_wins = ridge.predict(X_test_scaled)

current_wins = test_df['wins'].values
games_played = test_df['games_played'].values
remaining_games = 82 - games_played

final_wins = current_wins + predicted_remaining_wins
final_wins = np.round(final_wins).astype(int)
final_wins = np.clip(final_wins, 0, 82)
test_df['final_wins'] = final_wins
test_df['final_losses'] = 82 - final_wins
test_df['final_win_pct'] = np.round(final_wins / 82, 3)

#test_df.to_csv("data/csv/predicted_data.csv", index=False)
