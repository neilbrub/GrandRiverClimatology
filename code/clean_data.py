import os
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm

from configs import data_file_configs

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
    parser = argparse.ArgumentParser(prog='clean_data.py')
    parser.add_argument('config', help='Config key in data_file_configs')
    args = parser.parse_args()
    cfg_key = args.config
    if cfg_key not in data_file_configs: raise KeyError(cfg_key)

    input_file = '../data/raw/1996-2004.xlsx'
    
    sheet_name = data_file_configs[cfg_key]['sheet_name']
    cols = data_file_configs[cfg_key]['cols']
    header_row = data_file_configs[cfg_key]['header_row']
    header_names = data_file_configs[cfg_key]['header_names']
    range_limits = data_file_configs[cfg_key]['range_limits']

    output_file = '../data/processed/' + data_file_configs[cfg_key]['output_fname'] + '.xlsx'
    output_dir = '/'.join(output_file.split('/')[:-1])

    if not os.path.exists(output_dir): os.makedirs(output_dir)

    df = pd.read_excel(input_file, sheet_name=sheet_name, header=header_row,
        usecols=cols, names=header_names)
    
    filterBad(df, header_names[1:], range_limits=range_limits)

    df.to_excel(output_file)


if __name__ == "__main__": main()