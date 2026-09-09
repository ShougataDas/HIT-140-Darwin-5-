import pandas as pd

std  = pd.read_csv(r"C:\Users\dasso\OneDrive\Desktop\Data Science Project\standard.csv", skiprows=2)
misc = pd.read_csv(r"C:\Users\dasso\OneDrive\Desktop\Data Science Project\misc.csv",     skiprows=1)

for d in (std, misc):
    d.drop(d[d["Player"].isna()].index, inplace=True)

df = std.merge(misc, on=["Player", "Squad"], how="inner", suffixes=("", "_m"))

df = df[df["Pos"] != "GK"]
df = df[df["Min"] >= 90]

df["fouls_per_90"] = df["Fls"] / df["Min"] * 90
df["age_group"] = pd.cut(df["Age"], bins=[0, 23, 29, 99],
                         labels=["Young", "Peak", "Veteran"])

df[["Player","Squad","Pos","Age","age_group","Min","Fls","fouls_per_90"]] \
  .to_csv(r"C:\Users\dasso\OneDrive\Desktop\Data Science Project\wc2026_discipline.csv", index=False)