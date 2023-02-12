import os
import numpy as np
import pandas as pd
from tqdm import tqdm


def filterBad(df, col_names, range_limits=[-1, 35], fill_val=np.nan):
    """
    Duck-typing approach to converting values to numbers.
    Handles out-of-range numeric values as well as non-number values,
    e.g. '              ---' or '                .'
    """
    for col in col_names:
        print(f"\nProcessing colum {col}")
        for i, val in tqdm(enumerate(df[col])):
            try:
                set_val = np.float32(val)
                if set_val < range_limits[0] or set_val > range_limits[1]: set_val = fill_val
                df.loc[i, col] = set_val
            except ValueError:
                df.loc[i, col] = fill_val


def main():
    input_file = '../data/raw/2001-2010.xlsx'
    sheet_name = '2001-2010'
    cols = 'D:H'
    header_row = 1

    range_limits = [-0.5, 35]

    output_file = '../data/processed/2001-2010_cutoff_neghalf_35.xlsx'
    output_dir = '/'.join(output_file.split('/')[:-1])

    if not os.path.exists(output_dir): os.makedirs(output_dir)


    header_names = ['Date/Time', 'Bridgeport', 'Blair', 'Glen_Morris', 'Road_32']

    df = pd.read_excel(input_file, sheet_name=sheet_name, header=header_row,
        usecols=cols, names=header_names)
    
    filterBad(df, header_names[1:], range_limits=range_limits)

    df.to_excel(output_file)


if __name__ == "__main__": main()