# %%
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_many

dfs = load_many(all=True)

rows = []
for city, df in dfs.items():
    df["DTR"] = df["Max Temp"] - df["Min Temp"]
    df["city"] = city
    rows.append(df[["DTR", "city"]])

full = pd.concat(rows)

plt.figure(figsize=(12, 6))
sns.histplot(
    data=full,
    x="DTR",
    hue="city",
    kde=True,
    element="step",
    common_norm=False,
)
plt.title("Distribution of Diurnal Temperature Range")
plt.savefig("./output/hist_plot.pdf", bbox_inches="tight")
plt.show()

# %%
