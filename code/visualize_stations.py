import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def identify_nan_windows(data):
    nan_idcs = np.where(np.isnan(data))[0]
    nan_windows = []
    current_window = [-1, -1]
    last_idx = None
    for idx in nan_idcs:
        if last_idx != idx - 1:
            # Implications:
            #   1. Start of a new window
            #   2. End of previous window (unless start of sequence)

            if last_idx:
                # Mark end of last window & save
                current_window[1] = last_idx
                nan_windows.append(copy.copy(current_window))
                current_window = [-1, -1]
            
            # Mark start of new window
            current_window[0] = idx


        last_idx = idx
    
    return nan_windows


def plot_series(x_series, y_series, ax, label=""):
    """
    Plot series & shade nodata segments 
    """
    y_data = y_series.to_numpy()
    # data_max = np.nanmax(y_data)
    data_max = 30
    # data_min = np.nanmin(y_data)
    data_min = 0

    ax.plot(x_series, y_series, label=label, alpha=0.8)

    # nan_windows = identify_nan_windows(y_data)
    # for start, end in nan_windows:
    #     ax.fill_betweenx([data_min, data_max], x_series[start], x_series[end], alpha=0.2, color='k')



"""
Change things here
"""
def main():

    # Point this to processed spreadsheet
    excel_filpath = 'data/processed/2001-2010_cutoff_neghalf_35.xlsx'
    base_dir = '../'
    

    data = pd.read_excel(base_dir + excel_filpath, index_col=0)

    fig, ax = plt.subplots(figsize=(14, 7))

    plot_series(data['Date/Time'], data['Bridgeport'], ax, label="Bridgeport")
    plot_series(data['Date/Time'], data['Blair'], ax, label="Blair")
    # plot_series(data['Date/Time'], data['Glen_Morris'], ax, label="Glen Morris")
    plot_series(data['Date/Time'], data['Road_32'], ax, label="Road 32")
    ax.legend()

    plt.show()




if __name__ == "__main__": main()