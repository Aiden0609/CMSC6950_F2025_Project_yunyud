# Climate Extremes Analysis – St. John's and Other Canadian Cities (1994–2025)

## Overview
This project analyzes long-term temperature and precipitation variability in St. John’s, Newfoundland, and compares it with other major Canadian cities using Environment Canada’s historical climate dataset.  
The analysis focuses on identifying and visualizing **extreme-temperature events** through standardized climate indices — particularly the **Warm Spell Duration Index (WSDI)** and **Cold Spell Duration Index (CSDI)** — based on ETCCDI (Expert Team on Climate Change Detection and Indices) definitions.  

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

## How to Run

### 1. Clone the repository and change into its directory.
### 2. Set up environment and install dependencies

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
```bash
pip install -r requirements.txt
```

### 3. Download data
```bash
cd ./data/
bash downloadDaily.sh
```

### 4. Generate first plot
```bash
cd ..
python main.py
```