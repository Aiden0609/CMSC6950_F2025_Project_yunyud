# %%
import datetime
import matplotlib.pyplot as plt
from utils import load_single
from computeSDI import compute_wsdi

# Excluding Toronto due to lack of data
cities = ["StJohns", "Montreal", "Calgary", "Vancouver"]
year = 2024

city_dfs = {}
for city in cities:
    df = load_single(city)
    df_ext = compute_wsdi(df)
    city_dfs[city] = df_ext[df_ext["Year"] == year]

city_spells = {}

for city, df_year in city_dfs.items():
    spells = []
    for sid, grp in df_year.groupby("spell_id"):
        if sid == -1:
            continue
        start = grp["doy"].min()
        end = grp["doy"].max()
        spells.append((start, end))
    city_spells[city] = spells

plt.figure(figsize=(14, 6))

for i, city in enumerate(cities):
    spells = city_spells[city]

    for (s, e) in spells:
        plt.hlines(
            y=i,
            xmin=s,
            xmax=e,
            colors=f"C{i}",
            linewidth=8
        )

    plt.text(-10, i, city, va="center", ha="right", fontsize=10)

plt.yticks([])
doy_ticks = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
date_labels = [(datetime.date(2020, 1, 1) +
                datetime.timedelta(days=d-1)).strftime("%b %d")
               for d in doy_ticks]
plt.xticks(doy_ticks, date_labels)
plt.xlabel("Day of Year")
plt.title(f"Warm Spell Timeline for year {year}")
plt.xlim(0, 366)
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("./output/wsd_timeline.pdf", bbox_inches="tight")
plt.show()

# %%
