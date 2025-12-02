# %%
import seaborn as sns
import matplotlib.pyplot as plt
from utils import load_many, compute_yearly_extremes
import pandas as pd

dfs = load_many(all=True)

rows = []
for city, df in dfs.items():
    df = df[df["Year"].between(2003, 2024)].copy()
    yearly = compute_yearly_extremes(df)
    yearly["city"] = city
    rows.append(yearly)

full = pd.concat(rows)

fig, axes = plt.subplots(2, 1, figsize=(10, 12), sharex=True)

sns.boxplot(
    data=full, x="city",
    y="Max Temp", ax=axes[0]
)
axes[0].set_title("Historical Annual Extreme Maximum Temperature \n 2003-2024")

sns.boxplot(
    data=full, x="city",
    y="Min Temp", ax=axes[1]
)
axes[1].set_title("Historical Annual Extreme Minimum Temperature \n 2003-2024")

plt.tight_layout()
plt.savefig("./output/box_plot.pdf", bbox_inches="tight")
plt.show()


# %%
