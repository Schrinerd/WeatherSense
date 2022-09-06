import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from creds import output_loc,figsaveloc

inside_temp_path = output_loc + r'/inside_temps.csv'
scrape_temp_path = output_loc + r'/scraped_temps.csv'

dfmtr = mdates.DateFormatter('%-m/%-d %-I%p')

def plot_temps(show=False):
    temp_df = pd.read_csv(inside_temp_path, header=0,names=['Time','Temp']).tail(1000)
    temp_df['TimeF'] = pd.to_datetime(temp_df['Time'],unit='s')\
        .dt.tz_localize("UTC")\
        .dt.tz_convert("US/Eastern")\
        .dt.tz_localize(None) # I fucking hate datetimes
    s_temp_df = pd.read_csv(scrape_temp_path, header=0,names=['Time','Temp','Wind','Code','Pressure','Humidity']).tail(1000)
    s_temp_df['TimeF'] = pd.to_datetime(s_temp_df['Time'],unit='s')\
        .dt.tz_localize("UTC")\
        .dt.tz_convert("US/Eastern")\
        .dt.tz_localize(None) # I fucking hate datetimes
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(temp_df['TimeF'],temp_df['Temp'], label = 'Apartment')
    ax.plot(s_temp_df['TimeF'], s_temp_df['Temp'], label = 'Outside')
    ax.xaxis.set_major_formatter(dfmtr)
    ax.legend()
    ax.set_ylim(0,110)
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature, $^\circ$F')
    ax.set_title("Apartment and Outside Temperature")
    if show==True:
        plt.show()
    else:
        plt.savefig(figsaveloc)


plot_temps()


