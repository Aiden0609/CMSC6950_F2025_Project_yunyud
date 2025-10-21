import os

import matplotlib.pyplot as plt
import pandas as pd

from preprocessing import preprocessingDf


METRICS = ["Max Temp (°C)", "Min Temp (°C)"]


def plotMonthly(
    path: str = "./data/csv",
    stationId: int = 6720,
    outputPath: str= None,
    ):
    df = preprocessingDf(path=path, stationId=stationId)
   
    df_plot = df.loc[:, ['Year', 'Month', *METRICS]]
    
    df_plot['Month'] = pd.to_numeric(df_plot['Month'])

    df_monthly = (
        df_plot
        .groupby(['Year', 'Month'], as_index=False)
        .agg({'Max Temp (°C)': 'mean', 'Min Temp (°C)': 'mean'})
    )
    fig, ax = plt.subplots(figsize=(10, 6))

    for year, data in df_monthly.groupby('Year'):
        ax.plot(data['Month'], data['Max Temp (°C)'], label=f'{year} - Max')
        ax.plot(data['Month'], data['Min Temp (°C)'], linestyle='--', label=f'{year} - Min')

    ax.set_title('Monthly Average Max & Min Temperatures by Year')
    ax.set_xlabel('Month')
    ax.set_ylabel('Temperature (°C)')
    ax.legend()
    ax.grid(True)
    
    os.makedirs(outputPath, exist_ok=True)
    fig.savefig(os.path.join(outputPath, 'first_plot.png'), dpi=300, bbox_inches='tight')
    
    plt.show()
