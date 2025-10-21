#!/bin/bash

# timeframe=2 -- daily interval

station=6720
start_year=1994
end_year=2012
base="https://climate.weather.gc.ca/climate_data/bulk_data_e.html"

mkdir ./csv/
for year in $(seq "$start_year" "$end_year"); do
  echo "Downloading year ${year}, station ${station}"
  url="${base}?format=csv&stationID=${station}&Year=${year}&Month=1&Day=1&timeframe=2&submit=Download+Data"

  wget -nc -O "./csv/station_${station}_daily_${year}.csv" "$url"
done

