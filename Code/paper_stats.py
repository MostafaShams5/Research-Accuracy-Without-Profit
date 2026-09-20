import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.diagnostic import breaks_cusumolsresid

def main():
    print("=== 1. DESCRIPTIVE STATISTICS (Table 0) ===")
    df = pd.read_csv('Data/master_feature_table.csv')
    print(f"Total Matches: {len(df)}")
    print(df['FTR'].value_counts(normalize=True) * 100)

    print("\n=== 2. COVID-2020 HOME ADVANTAGE EVAPORATION ===")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    home_win_pct = df.groupby('Year')['FTR'].apply(lambda x: (x == 'H').mean())
    print(home_win_pct.tail(6))

    print("\n=== 3. STRUCTURAL BREAK TEST (CUSUM) ===")
    try:
        roi_df = pd.read_csv('results_XGBoost.csv')
        seasonal = roi_df.groupby('Season').agg(PnL=('PnL', 'sum'), Bets=('PnL', 'count')).reset_index()
        seasonal['ROI'] = seasonal['PnL'] / (seasonal['Bets'] * 100)
        
        # OLS regression of ROI against time
        X = sm.add_constant(np.arange(len(seasonal)))
        y = seasonal['ROI'].values
        model = sm.OLS(y, X).fit()
        
        # CUSUM test for parameter stability (structural break)
        cusum_stat, p_val, crit = breaks_cusumolsresid(model.resid)
        print(f"CUSUM Test p-value: {p_val:.4f}")
        if p_val < 0.05:
            print("Result: Statistically significant structural break found!")
        else:
            print("Result: No definitive single structural break at 95% confidence.")
    except FileNotFoundError:
        print("Run backtesting_ml_strategies.py first to generate results_XGBoost.csv")

    print("\n=== 4. KELLY CRITERION: CALIBRATED VS UNCALIBRATED ===")
    try:
        def simulate_kelly(df_path, fraction=1.0):
            df = pd.read_csv(df_path)
            df['b'] = df['Bet_Odds'] - 1
            df['p'] = df.apply(lambda r: r['HomeProb'] if r['Predicted']=='H' else (r['DrawProb'] if r['Predicted']=='D' else r['AwayProb']), axis=1)
            df['q'] = 1 - df['p']
            df['Kelly_Fraction'] = (df['b'] * df['p'] - df['q']) / df['b']
            df['Kelly_Fraction'] = df['Kelly_Fraction'].clip(lower=0, upper=0.25)
            
            bankroll = 10000
            for idx, row in df.iterrows():
                if row['Kelly_Fraction'] > 0:
                    bet = bankroll * (row['Kelly_Fraction'] * fraction)
                    bankroll += bet * row['b'] if row['Won'] else -bet
            return bankroll

        print("Base XGBoost (Uncalibrated):")
        print(f"  Full Kelly: ${simulate_kelly('results_XGBoost.csv', 1.0):.2f}")
        print(f"  0.1  Kelly: ${simulate_kelly('results_XGBoost.csv', 0.1):.2f}")
        
        print("\nCalibrated XGBoost (Isotonic):")
        print(f"  Full Kelly: ${simulate_kelly('results_XGBoost_Calibrated.csv', 1.0):.2f}")
        print(f"  0.1  Kelly: ${simulate_kelly('results_XGBoost_Calibrated.csv', 0.1):.2f}")
    except FileNotFoundError:
        print("Please run the backtests first to generate the CSV results.")

if __name__ == "__main__":
    main()
