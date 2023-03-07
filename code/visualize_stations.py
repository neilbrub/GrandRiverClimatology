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


def plot_series(x_series, y_series, ax, label="", shade_nodata=False):
    """
    Plot series & shade nodata segments 
    """
    ax.plot(x_series, y_series, label=label, alpha=0.8)

    if shade_nodata:
        y_data = y_series.to_numpy()
        data_max = np.nanmax(y_data)
        data_min = np.nanmin(y_data)
        data_max = 35
        data_min = -0.5

        nan_windows = identify_nan_windows(y_data)
        for start, end in nan_windows:
            ax.fill_betweenx([data_min, data_max], x_series[start], x_series[end], alpha=0.2, color='k')



"""
Change things here
"""
def main():

    base_dir = ''
    

    # For combined sheets separated by column:
    excel_filpath = 'data/processed/merged_data_neghalf_35.xlsx'
    data_df = pd.read_excel(base_dir + excel_filpath, index_col=0)
    stn_names = ['bridgeport', 'blair', 'glenmorris', 'road32']
    data_dts = [data_df.index for i in stn_names]
    stn_data = [data_df[col] for col in stn_names] 


    # # For individual sheets:
    # data_base_fp = base_dir + 'data/processed/1996-2004_'
    # sheet_fps = ['blair_neghalf_35.xlsx', 'bridgeport_neghalf_35.xlsx',
    #              'glenmorris_neghalf_35.xlsx', 'road32_neghalf_35.xlsx']
    
    # stn_names = ['Bridgeport', 'Blair', 'Glen_Morris', 'Road_32']
    # stn_data = []
    # data_dts = []
    
    # for sheet_fp in sheet_fps:
    #     data_df = pd.read_excel(data_base_fp + sheet_fp, index_col=0)
    #     data_dts.append(data_df['DATE'])
    #     stn_data.append(data_df['PARM_VAL'])


    # plt.rc('font', size=20)
    # plt.rc('axes', labelsize=18)
    # plt.rc('xtick', labelsize=18)
    # plt.rc('ytick', labelsize=18)
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, data in enumerate(stn_data):
        plot_series(data_dts[i], data, ax, label=stn_names[i])

    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature ($\degree$C)")

    plt.title("Grand River Hourly Water Temperatures, 1996-2010")

    # plt.savefig(base_dir + 'plots/series/1996-2010_4stns_clipped.png')
    plt.show()




if __name__ == "__main__": main()