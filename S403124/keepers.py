import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# ---------- STEP 1: Load ----------
df = pd.read_csv("keepers.csv", skiprows=1)
df = df.dropna(subset=["Player"])
df = df.drop(columns=["Matches", "-9999"], errors="ignore")
df = df.rename(columns={"Save%": "Save_Pct_Shots", "Save%.1": "Save_Pct_Penalties"})

numeric_cols = ["Age", "MP", "Starts", "Min", "GA", "SoTA", "Saves"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------- STEP 2: Build region grouping ----------
df["Country"] = df["Squad"].apply(lambda x: x.split(" ", 1)[1])

print("Countries found in your data:")
print(sorted(df["Country"].unique()))
print()  # check this list once - confirm Bosnia's exact spelling below matches

uefa_teams = {
    "Austria", "Belgium", "Croatia", "England", "France", "Germany",
    "Netherlands", "Norway", "Portugal", "Scotland", "Spain", "Switzerland",
    "Bosnia and Herzegovina", "Bosnia–Herz", "Czechia", "Sweden", "Türkiye"
}

df["region"] = df["Country"].apply(lambda c: "European" if c in uefa_teams else "Rest of World")

# ---------- STEP 3: Filter to population ----------
gk = df[(df["Min"] >= 90) & (df["SoTA"] > 0)].copy()
print(f"Total goalkeepers: {len(df)} | Excluded: {len(df) - len(gk)} | Final sample: {len(gk)}\n")

# ---------- STEP 4: Compute save % ----------
gk["save_pct"] = gk["Saves"] / gk["SoTA"] * 100

# ---------- STEP 5: Descriptive statistics ----------
print("--- Group sizes ---")
print(gk["region"].value_counts(), "\n")

print("--- Descriptive statistics (save %) ---")
desc = gk.groupby("region")["save_pct"].agg(["count", "mean", "median", "std", "min", "max"])
print(desc.round(2), "\n")

# ---------- STEP 6: Confidence intervals ----------
def confidence_interval(sample, conf=0.95):
    n = len(sample)
    mean = sample.mean()
    se = stats.sem(sample)
    margin = se * stats.t.ppf((1 + conf) / 2, n - 1)
    return mean, mean - margin, mean + margin

print("--- 95% Confidence Intervals ---")
for region, sub in gk.groupby("region"):
    mean, lo, hi = confidence_interval(sub["save_pct"])
    print(f"{region}: mean={mean:.2f}%, 95% CI=({lo:.2f}%, {hi:.2f}%), n={len(sub)}")
print()

# ---------- STEP 7: Two-sample t-test ----------
euro = gk[gk["region"] == "European"]["save_pct"]
rest = gk[gk["region"] == "Rest of World"]["save_pct"]
t_stat, p_value = stats.ttest_ind(euro, rest, equal_var=False)

print("--- Welch's Two-Sample t-Test ---")
print(f"t-statistic = {t_stat:.4f}")
print(f"p-value     = {p_value:.4f}")
print("Significant" if p_value < 0.05 else "NOT significant", "at alpha=0.05")

# ---------- STEP 8: Save cleaned dataset ----------
gk.to_csv("wc2026_goalkeeping_cleaned.csv", index=False)
print("\nSaved: wc2026_goalkeeping_cleaned.csv")

plt.figure(figsize=(6,5))
gk.boxplot(column="save_pct", by="region")
plt.title("Goalkeeper Save % by Region")
plt.suptitle("")
plt.ylabel("Save %")
plt.xlabel("Region")
plt.savefig("save_pct_boxplot.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: save_pct_boxplot.png")