# Climate Extremes Analysis – St. John's and Other Canadian Cities (1994–2025)

## Overview
This project analyzes long-term temperature and precipitation variability in St. John’s, Newfoundland, and compares it with other major Canadian cities using Environment Canada’s historical climate dataset.  
The analysis focuses on identifying and visualizing **extreme-temperature events** through  **Warm Spell Duration Index (WSDI)** and **Hot day counts** — based on copernicus definitions.  

In addition to temperature extremes, the project examines **spatial**, **temporal**, and **trend-based** patterns using both statistical and visual methods.


---

## Dataset
**Source:** [Environment and Climate Change Canada – Historical Climate Data](https://climate.weather.gc.ca/historical_data/search_historic_data_e.html)

**Variables used**
- Date (Year, Month, Day)
- Max Temp (°C), Min Temp (°C), Mean Temp (°C)
- Total Precipitation (mm)
- Station metadata (Name, Latitude, Longitude)

**Time period:** 1994–2025 (daily data)

Data are downloaded in `.csv` format using official Environment Canada batch download scripts.

---

## How to Reproduce Results

### 1. Clone the repository and set up a virtual environment
```bash
git clone <this-repo-url>
cd CMSC6950_F2025_Project_yunyud
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. (Optional but recommended) Run tests
```bash
pytest tests/
```

### 3. Download raw data from Environment Canada

The project uses Environment Canada’s bulk-download interface.  
From the repository root:
```bash
cd scripts/download
bash downloadStJohns.sh
bash downloadMontreal.sh
bash downloadCalg.sh
bash downloadVanc.sh
bash downloadTrtCity.sh
cd ../..
```

Daily data for each city is saved to `data/raw/`.

### 4. Preprocess raw data
```bash
mkdir data/processed/
cd scripts
python preprocessing.py
cd ..
```

This will create/update processed files in `data/processed/` for all cities.

### 5. Generate figures and analyses

All analysis scripts assume processed data in `data/processed/`. Examples:
```bash
python box_plot.py

python hist_plot.py
```
```bash
python line_plot.py
python line_plot.py --city Vancouver
```
```bash
python wsd_timeline.py
python wsdi_heatmap.py

python geomap.py
```

Each script will display graph and save outputs into `output/`.

## Reference
 1. https://www.climdex.org/learn/indices/#index-WSDI
 2. https://drought.emergency.copernicus.eu/data/factsheets/factsheet_warmColdSpellIndex.pdf
