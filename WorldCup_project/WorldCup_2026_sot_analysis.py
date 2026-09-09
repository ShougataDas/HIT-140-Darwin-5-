import pandas as pd

# Load the dataset
df = pd.read_excel("Worlcup2026_sot.xlsx")
df = df.dropna(subset=["SoT/90", "Stage"])
# Display the first five rows
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nNumber of teams:")
print(len(df))

print("\nStage counts:")
print(df["Stage"].value_counts())

# DATA PREPARATION AND SAMPLING

knockout = df[df["Stage"] == "Knockout"]["SoT/90"]
group = df[df["Stage"] == "Group"]["SoT/90"]

print("Knockout teams:", len(knockout))
print("Group-stage teams:", len(group))

# DESCRIPTIVE SATISTICS

print("Knockout teams")
print(knockout.describe())

print("\nGroup-stage teams")
print(group.describe())

# 95% CONFIDENCE INTERVAL

from scipy import stats
import numpy as np

def confidence_interval(data):
    mean = np.mean(data)
    se = stats.sem(data)
    ci = stats.t.interval(
        0.95,
        df=len(data)-1,
        loc=mean,
        scale=se
    )
    return mean, ci

print(confidence_interval(knockout))
print(confidence_interval(group))

# TWO-SAMPLE T-TEST

from scipy.stats import ttest_ind

t_stat, p_value = ttest_ind(
    knockout,
    group,
    equal_var=False
)

print("t-statistic:", t_stat)
print("p-value:", p_value)

# VISUALIZATION (BOX PLOT)

import matplotlib.pyplot as plt

# Separate the two groups
knockout = df[df["Stage"] == "Knockout"]["SoT/90"]
group = df[df["Stage"] == "Group"]["SoT/90"]

# Create boxplot
fig, ax = plt.subplots(figsize=(8, 6))

box = ax.boxplot(
    [knockout, group],
    tick_labels=["Knockout Stage", "Group Stage"],
    patch_artist=True
)

# Add colour
box["boxes"][0].set_facecolor("#4C78A8")
box["boxes"][1].set_facecolor("#F58518")

# Make median lines stand out
for median in box["medians"]:
    median.set_color("black")
    median.set_linewidth(2)

ax.set_title(
    "Shots on Target per 90 by Tournament Stage",
    fontsize=15,
    fontweight="bold"
)

ax.set_ylabel("Shots on Target per 90")
ax.set_xlabel("Tournament Stage")

ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

# 95% CI
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Calculate means
means = [
    knockout.mean(),
    group.mean()
]

# Calculate 95% confidence intervals
ci_knockout = stats.t.interval(
    0.95,
    len(knockout) - 1,
    loc=knockout.mean(),
    scale=stats.sem(knockout)
)

ci_group = stats.t.interval(
    0.95,
    len(group) - 1,
    loc=group.mean(),
    scale=stats.sem(group)
)

# Calculate error amounts
errors = [
    means[0] - ci_knockout[0],
    means[1] - ci_group[0]
]

# Create chart
fig, ax = plt.subplots(figsize=(8, 6))

bars = ax.bar(
    ["Knockout Stage", "Group Stage"],
    means,
    yerr=errors,
    capsize=8,
    color=["#4C78A8", "#F58518"],
    edgecolor="black"
)

ax.set_title(
    "Average Shots on Target per 90 with 95% CI",
    fontsize=15,
    fontweight="bold"
)

ax.set_ylabel("Average Shots on Target per 90")
ax.set_xlabel("Tournament Stage")

ax.grid(axis="y", alpha=0.3)

# Add values above bars
for bar, value in zip(bars, means):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        f"{value:.2f}",
        ha="center",
        fontweight="bold"
    )

plt.tight_layout()
plt.show()