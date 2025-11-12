#!/bin/bash

# timeframe=2 -- daily interval

base="https://climate.weather.gc.ca/climate_data/bulk_data_e.html"

mkdir -p ./StJohns/

download_range () {
  station="$1"; start_year="$2"; end_year="$3"
  for year in $(seq "$start_year" "$end_year"); do
    echo "Downloading year ${year}, station ${station}"
    url="${base}?format=csv&stationID=${station}&Year=${year}&Month=1&Day=1&timeframe=2&submit=Download+Data"
    wget -nc -O "./StJohns/station_${station}_daily_${year}.csv" "$url"
  done
}

# 6720: 1994–2012
download_range 6720 1994 2012

# 50089: 2012–2025
download_range 50089 2012 2025