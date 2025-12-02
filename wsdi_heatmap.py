# %%
import seaborn as sns
import matplotlib.pyplot as plt
from computeSDI import compute_wsdi
from utils import load_single

city = "StJohns"

df = load_single(city)
df_ext = compute_wsdi(df)

heat = df_ext.groupby(["Year", "Month"])["hot"].sum().reset_index()
pivot = heat.pivot(index="Month", columns="Year", values="hot")

plt.figure(figsize=(14, 5))
sns.heatmap(pivot, cmap="YlOrRd")
plt.title(f"{city} — Hot Day Monthly Heatmap")
plt.savefig("./output/wsdi_heatmap.pdf", bbox_inches="tight")
plt.show()


# %%
