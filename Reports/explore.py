import pandas as pd
import numpy as np
from scipy import stats

# 1. Load Data
df = pd.read_csv('Reports/results_XGBoost.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

# 2. Season-by-Season ROI and Structural Break (2015)
seasonal = df.groupby('Season').agg(
    Bets=('PnL', 'count'),
    PnL=('PnL', 'sum'),
    Accuracy=('Won', 'mean')
).reset_index()
seasonal['ROI'] = seasonal['PnL'] / (seasonal['Bets'] * 100)

print("=== SEASONAL ROI ===")
print(seasonal[['Season', 'ROI', 'Accuracy']])

roi_before_2015 = seasonal[seasonal['Season'] < 2015]['ROI']
roi_after_2015 = seasonal[seasonal['Season'] >= 2015]['ROI']
t_stat, p_val = stats.ttest_ind(roi_before_2015, roi_after_2015, equal_var=False)
print(f"\nWelch's t-test for Structural Break (Before vs After 2015) p-value: {p_val:.4f}")

# 3. COVID Effect (Home Advantage Drop in 2020)
raw = pd.read_csv('Data/master_feature_table.csv')
raw['Date'] = pd.to_datetime(raw['Date'])
raw['Year'] = raw['Date'].dt.year # rough season approx
home_win_pct = raw.groupby('Year')['FTR'].apply(lambda x: (x=='H').mean())
print("\n=== HOME WIN % BY YEAR (COVID check) ===")
print(home_win_pct.tail(6))

# 4. Fractional Kelly Simulation
df['b'] = df['Bet_Odds'] - 1
df['p'] = df.apply(lambda row: row['HomeProb'] if row['Predicted']=='H' else (row['DrawProb'] if row['Predicted']=='D' else row['AwayProb']), axis=1)
df['q'] = 1 - df['p']
df['Kelly_Fraction'] = (df['b'] * df['p'] - df['q']) / df['b']
df['Kelly_Fraction'] = df['Kelly_Fraction'].clip(lower=0, upper=0.25)

def simulate_bankroll(f_kelly_multiplier=1.0):
    bankroll = 10000
    for idx, row in df.iterrows():
        if row['Kelly_Fraction'] > 0:
            bet_size = bankroll * (row['Kelly_Fraction'] * f_kelly_multiplier)
            if row['Won']:
                bankroll += bet_size * row['b']
            else:
                bankroll -= bet_size
    return bankroll

print("\n=== KELLY CRITERION ANALYSIS ===")
print(f"Full Kelly Final Bankroll: ${simulate_bankroll(1.0):.2f}")
print(f"Half Kelly (0.5) Final Bankroll: ${simulate_bankroll(0.5):.2f}")
print(f"Quarter Kelly (0.25) Final Bankroll: ${simulate_bankroll(0.25):.2f}")
print(f"10% Kelly (0.1) Final Bankroll: ${simulate_bankroll(0.1):.2f}")

