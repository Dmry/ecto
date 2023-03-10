import pandas as pd
import numpy as np

def read_imp(infile, sep):
    return pd.read_csv(infile, skiprows=3, sep=sep, names=["time", "chan_a", "chan_c", "chan_x"], dtype={"time" : np.float32, "chan_a" : np.float32, "chan_c" : np.float32}, engine="pyarrow")

def read(infile):
    try:
        df = read_imp(infile, sep=",")
    except:
        df = read_imp(infile, sep=";")

    return df

def clean(df):
    df = df[2:]
    df.reset_index(inplace=True)

    # Convert string values to numeric
    df.chan_a = pd.to_numeric(df.chan_a)
    df.chan_c = pd.to_numeric(df.chan_c)