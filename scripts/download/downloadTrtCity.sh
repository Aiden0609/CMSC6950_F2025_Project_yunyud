#!/usr/bin/env bash

# Configuration
BASE="https://climate.weather.gc.ca/climate_data/bulk_data_e.html"
CITY="TorontoCity" 
OUTDIR="../../data/raw/${CITY}"
TIMEFRAME=2     # daily

mkdir -p "${OUTDIR}"

download_range() {
    local station_id="$1"
    local start_year="$2"
    local end_year="$3"

    for year in $(seq "${start_year}" "${end_year}"); do
        echo "Downloading ${CITY} | Station ${station_id} | Year ${year}"

        local outfile="${OUTDIR}/${CITY}_${station_id}_${year}.csv"

        if [[ -f "${outfile}" ]]; then
            continue
        fi

        local url="${BASE}?format=csv&stationID=${station_id}&Year=${year}&Month=1&Day=1&timeframe=${TIMEFRAME}&submit=Download+Data"

        wget -q --show-progress -O "${outfile}" "${url}"

    done
}

# Toronto City
download_range 31688 2002 2025
