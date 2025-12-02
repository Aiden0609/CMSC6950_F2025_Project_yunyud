# %%
import matplotlib.pyplot as plt
from utils import load_single, compute_monthly
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--city", default="Calgary")

args = parser.parse_args()

city = args.city

c1 = "StJohns"
c2 = args.city
year = 2024            # 2003-2024

df1 = load_single(c1)
df2 = load_single(c2)

df1 = df1[df1["Year"] == year]
df2 = df2[df2["Year"] == year]

if df1.empty or df2.empty:
    raise ValueError("One of the cities has no data for this year.")

mo1 = compute_monthly(df1)
mo2 = compute_monthly(df2)


plt.figure(figsize=(12, 7))


# Temperature part
ax1 = plt.gca()

ax1.plot(mo1["Month"], mo1["Max Temp"],
         color="tab:blue", linewidth=2,
         label=f"{c1} Max Temp")
ax1.plot(mo1["Month"], mo1["Min Temp"],
         color="tab:blue", linewidth=2, linestyle=":",
         label=f"{c1} Min Temp")

ax1.plot(mo2["Month"], mo2["Max Temp"],
         color="tab:red", linewidth=2,
         label=f"{c2} Max Temp")
ax1.plot(mo2["Month"], mo2["Min Temp"],
         color="tab:red", linewidth=2, linestyle=":",
         label=f"{c2} Min Temp")

ax1.set_xlabel("Month")
ax1.set_ylabel("Temperature (°C)")
ax1.set_xticks(range(1, 13))
ax1.grid(alpha=0.25)

# Precip part
ax2 = ax1.twinx()

ax2.plot(mo1["Month"], mo1["Total Precip"],
         color="tab:blue", linewidth=2, linestyle="--",
         label=f"{c1} Precip")

ax2.plot(mo2["Month"], mo2["Total Precip"],
         color="tab:red", linewidth=2, linestyle="--",
         label=f"{c2} Precip")

ax2.set_ylabel("Total Monthly Precipitation")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title(f"Monthly Climate Comparison ({year}), {c1} vs {c2}")
plt.tight_layout()
plt.savefig(f"./output/line_plot_{c2}.pdf", bbox_inches="tight")
plt.show()

# %%
