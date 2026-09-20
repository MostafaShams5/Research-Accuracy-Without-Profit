from PIL import Image
import os
import glob

# Ordered list of figures as they appear in main.tex
figures = [
    "fig_confusion_matrices.png",
    "fig_bet_distribution.png",
    "fig_alpha_decay.png",
    "fig_temporal_roi.png",
    "fig_cumulative_wealth.png",
    "fig_kelly_vs_flat.png",
    "fig_calibration_curves.png",
    "fig_shap_summary.png",
    "plot_hist_XGBoost_AI.png",
    "plot_comparative_kde.png"
]

mapping = {}

for i, old_name in enumerate(figures):
    new_name = f"Figure_{i+1}.png"
    mapping[old_name] = new_name
    
    if os.path.exists(old_name):
        # Open and resize if needed
        img = Image.open(old_name)
        w, h = img.size
        
        # We need w >= 1500 and h >= 1200
        ratio = max(1.0, 1500.0/w, 1200.0/h)
        if ratio > 1.0:
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            
        img.save(new_name)
        print(f"Processed {old_name} -> {new_name} (Size: {img.size})")

# Update main.tex
with open("main.tex", "r") as f:
    tex_content = f.read()

for old_name, new_name in mapping.items():
    tex_content = tex_content.replace(old_name, new_name)

# Ensure "Corresponding author" is explicitly written for Snapp
# Let's add it directly to the author block if not already there, 
# or add a footnote-style mark. sn-jnl adds the envelope, but Snapp wants explicit text.
# Let's just modify the text to literally say "(Corresponding author)"
tex_content = tex_content.replace(r'\fnm{Mostafa} \sur{Shams}', r'\fnm{Mostafa} \sur{Shams} (Corresponding author)')

with open("main.tex", "w") as f:
    f.write(tex_content)
    
print("Updated main.tex")
