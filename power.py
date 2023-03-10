import numpy as np

from utility import pairwise
from input import Signal

def calc_power(chan_a : Signal, chan_c : Signal, time, envelope_time):
    i = (np.abs(time - envelope_time)).argmin()

    return chan_a[0:i] * chan_c[0:i]