
import numpy as np
import pandas as pd
from tqdm import tqdm

def binDataToReg(reg_df, irreg_timestamps, irreg_data, col_name):
    assert len(irreg_timestamps) == len(irreg_data)

    if col_name not in reg_df.columns: reg_df[col_name] = np.nan

    print(f"Aligning {col_name}")
    for i, ts in enumerate(tqdm(irreg_timestamps)):
        # Find closest regular timestamp & populate that row
        reg_idx = reg_df.index.searchsorted(ts)
        reg_df[col_name][reg_idx] = irreg_data[i]


def formatStnName(stn_in):
    return stn_in.replace('_', '').lower()


def main():
    base_dir = ''
    data_dir = base_dir + 'data/processed/'

    output_file = data_dir + 'merged_data.xlsx'

    files = {
        '1996': {
            'bridgeport': '1996-2004_bridgeport_neghalf_35.xlsx',
            'glenmorris': '1996-2004_glenmorris_neghalf_35.xlsx',
            'blair': '1996-2004_blair_neghalf_35.xlsx',
            'road32': '1996-2004_road32_neghalf_35.xlsx',
        }, 
        '2001': '2001-2010_cutoff_neghalf_35.xlsx'
    }

    # 1. Load all data sheets
    # 2. Identify min date from '96 and max date from 2010
    # 3. Create empty df with time spanning min & max date at consistent 1h interval
    # 4. For '96 sheets: For each station at a time, match entry to time bucket
    # 5. For 2001 sheet: For each target time bucket starting from earliest date in sheet,
    #    add data for all stations (overwriting any entries from '96)

    # 1 & 2. Load data & find min & max date
    data = {}
    min_date = None
    max_date = None

    for k, v in files.items():
        if k == '1996':
            data[k] = {}
            print("Loading 1996 sheets...")
            for stn, fp in tqdm(files[k].items()):
                data_df = pd.read_excel(data_dir + fp, index_col=0)
                data[k][stn] = data_df

                stn_min_date = data_df['DATE'].iloc[0]
                if not min_date or stn_min_date < min_date:
                    min_date = stn_min_date

        else:
            print("Loading 2001 sheet...")
            data_df = pd.read_excel(data_dir + v, index_col=0)
            data[k] = data_df

            max_date = data_df['Date/Time'].iloc[-1]


    reg_timestamps = pd.date_range(min_date, max_date, freq='H', inclusive='both', name='Timestamp')
    reg_df = pd.DataFrame(index=reg_timestamps)
    
    for stn, df in data['1996'].items():
        binDataToReg(reg_df, df['DATE'], df['PARM_VAL'], stn)

    for col in data['2001'].columns:
        if col != 'Date/Time':
            binDataToReg(reg_df, data['2001']['Date/Time'], data['2001'][col], formatStnName(col))

    reg_df.to_excel(output_file)


if __name__ == "__main__": main()