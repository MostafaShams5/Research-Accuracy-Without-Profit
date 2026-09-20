import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import matplotlib.pyplot as plt

df = pd.read_csv('data_sample.csv')
features = ['HomeOdds', 'DrawOdds', 'AwayOdds',
            'home_avg_pts', 'home_avg_gc', 'home_avg_s', 'home_avg_st', 'home_avg_c',
            'away_avg_pts', 'away_avg_gc', 'away_avg_s', 'away_avg_st', 'away_avg_c']

X = df[features].dropna()
y_map = {'H': 2, 'D': 1, 'A': 0}
y = df.loc[X.index, 'FTR'].map(y_map)

model = xgb.XGBClassifier(objective='multi:softprob', num_class=3, random_state=42, n_estimators=100)
model.fit(X, y)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

shap_vals_home = shap_values[2] if isinstance(shap_values, list) else shap_values[:, :, 2]
if shap_vals_home is None or len(shap_vals_home.shape) != 2:
    shap_vals_home = np.array(shap_values)

X_clean = X.copy()
X_clean.columns = [c.replace('_', ' ').title() for c in X.columns]
X_clean.rename(columns={'Homeodds': 'Home Odds', 'Drawodds': 'Draw Odds', 'Awayodds': 'Away Odds'}, inplace=True)

fig = plt.figure(figsize=(14, 10))
shap.summary_plot(shap_vals_home, X_clean, show=False, plot_type="bar", color='#0066CC')
ax = plt.gca()
ax.set_title("Feature Importance (SHAP)", fontsize=20, pad=20)
ax.set_xlabel("Mean Absolute SHAP Value (Impact on Prediction)", fontsize=16)
plt.tight_layout()
plt.savefig('../fig_shap_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print("Saved fig_shap_summary.png")
