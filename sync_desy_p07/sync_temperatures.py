#!/usr/bin/env python3

# Credits to Arthur Seiji Nishikawa and Giovani Gonçalves Ribamar


# The Script uses metadata files of diffraction rings images. To run,
# this script must be in the same directory of: .D5DT and .log files,
# and a folder named "metadata" containing all metadata files of the
# same measurement. If the measurement was divided in two, the user
# must join the metadata files from both pieces in the same folder
# ("metadata").

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from scipy.interpolate import interp1d
from scipy.optimize import golden
from pathlib import Path


def fetch_timestamp(fname):
    """
    Function to take the timestamp value from a Metadata file
    The metadata files comes from .tiff diffraction images
    """
    timestamp = None
    with open(fname, 'r') as f:
        for line in f:
            if 'timeStamp' in line:
                timestamp = float(line.split('=')[-1])
                break
    return timestamp


def parse_log_files(fnames):
    """
    Parse a log file taking the informations of: (i) Name (basename);
    (ii) acquisition index (number of the image); (iii) temperature given
    by the log file (np.nan substitutes "unknown" values)
    Return a pandas DataFrame
    """
    basename = []
    acqindex = []
    temp = []
    for fname in fnames:
        df = pd.read_csv(fname, delim_whitespace=True,
                         comment='!', header=None)
        basename += list(df[1])
        acqindex += list(df[2])
        temp += list(df[8].replace('unknown', np.nan).astype(float))
    return pd.DataFrame(dict(basename=basename, acqindex=acqindex, temp=temp))


def wrap_objective_time_shift(time_dil, temp_dil, time_mdata, temp_mdata):
    time2temp = interp1d(time_dil, temp_dil, bounds_error=False,
                         fill_value=0)

    def objective(time_shift):
        time_new = time_mdata - time_shift
        temp_new = time2temp(time_new)
        return ((temp_new - temp_mdata)**2).mean()

    return objective


if __name__ == '__main__':

    log_files = Path().glob("*.log")

    # Fetches metadata from all points, including fast acquisition
    timestamp_metadata = OrderedDict()
    for fpath in sorted(Path('metadata').glob('*.tif.metadata')):
        timestamp = fetch_timestamp(fpath)
        if timestamp is None:
            print(f'Could not find timeStamp in file {str(fpath)}')
            continue
        timestamp_metadata[str(fpath)] = timestamp

    df_temp = parse_log_files(log_files)
    df_temp['timestamp'] = np.nan
    image_number = []
    for index, row in df_temp.iterrows():
        fpath = Path('metadata',
                     f'{row["basename"]}-{row["acqindex"]:05d}.tif.metadata')
        try:
            timestamp = timestamp_metadata[str(fpath)]
        except KeyError:
            print(f'Could not find timeStamp in file {str(fpath)}')
            continue
        df_temp.loc[index, 'timestamp'] = timestamp

    timestamp_0 = df_temp.loc[0, 'timestamp']
    df_temp['time'] = df_temp['timestamp'] - timestamp_0

    dil_file = list(Path().glob("*.D5DT"))[0]

    df_dil = pd.read_csv(dil_file,
                         header=None, delim_whitespace=True)
    time2temp = interp1d(df_dil[0], df_dil[1], bounds_error=False,
                         fill_value=np.nan)

    objective = wrap_objective_time_shift(df_dil[0],
                                          df_dil[1],
                                          df_temp['time'],
                                          df_temp['temp'])

    t_min = min(df_temp['time'].min(), df_dil[0].min())
    t_max = max(df_temp['time'].max(), df_dil[0].max())
    # Determines time_shift by finding global minimum of objective function
    # created using wrap_objective_time_shift. Minimization is done using the
    # Golden Section Method to search for global minimum in the interval
    # (t_min, t_max)
    time_shift = golden(objective, brack=(t_min, t_max))

    # Corrects time
    time_corrected = np.array(list(timestamp_metadata.values())) \
        - timestamp_0 - time_shift

    # Plots stuff
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ax1, ax2 = axes[0, 0], axes[0, 1]
    gs = axes[1, 0].get_gridspec()
    axes[1, 0].remove()
    axes[1, 1].remove()
    ax3 = fig.add_subplot(gs[1, :])

    ax1.plot(df_dil[0], df_dil[1], 'r-', label="Dilatometry data")
    ax1.plot(df_temp['time'], df_temp['temp'], 'kx', label="Diffraction data")
    ax1.set_title('Raw')
    ax1.set_xlabel("Time (s)", size=15)
    ax1.set_ylabel("Temperature (°C)", size=15)
    ax1.legend()

    ax2.plot(df_dil[0], df_dil[1], 'r-', label="Dilatometry")
    ax2.plot(df_temp['time'] - time_shift, df_temp['temp'], 'kx',
             label="Diffraction")
    ax2.set_title('Slow mode acquisition points after correction')
    ax2.set_xlabel("Time (s)", size=15)
    ax2.set_ylabel("Temperature (°C)", size=15)
    ax2.legend()

    ax3.plot(df_dil[0], df_dil[1], 'r-', label="Dilatometry data")
    ax3.plot(time_corrected, time2temp(time_corrected),
             'kx', label="Diffraction data")

    ax3.set_xlabel('Time (s)', size=15)
    ax3.set_ylabel('Temperature (°C)', size=15)
    ax3.set_title('All points after correction')
    ax3.legend()

    sync_file = pd.DataFrame()
    sync_file["Image"] = [k.lstrip("metadata/").rstrip(".tif.metadata")
                          for k in timestamp_metadata.keys()]
    sync_file["Time(s)"] = time_corrected
    sync_file["Temperature(oC)"] = time2temp(time_corrected)

    name = sync_file["Image"][0].rstrip("_1-00001")

    sync_file.to_csv("./" + name + "_sync_file.txt", sep=";", index=None)

    fig.tight_layout()
    fig.savefig("./" + name + "_plot_sync_results.jpg", dpi=400)
    plt.show()
