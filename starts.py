import math
import logging

import numpy as np
import cupy as cp
from numpy.fft import ifftshift
from scipy.optimize import curve_fit

from utility import pairwise

'''
t: time
p: period in pi
'''
def sine(t, p):
    return 0.5*(np.cos((1/p)*t)+1)

def autocorr(t,x):
    logging.debug("Shifting")
    xp = ifftshift((x - np.average(x))/np.std(x))
    n, = xp.shape
    logging.debug("Slicing")
    xp = np.r_[xp[:n//2], np.zeros_like(xp), xp[n//2:]]
    logging.debug("Moving input from RAM to GPU")
    cxp = cp.asarray(xp)
    logging.debug("FFT")
    f = cp.fft.fft(cxp)
    del xp
    p = cp.absolute(f)**2
    del f
    logging.debug("iFFT")
    cpi = cp.fft.ifft(p)
    pi = cp.asnumpy(cpi)
    del p
    s = np.real(pi)[:n//2]/(np.arange(n//2)[::-1]+n//2)
    return s

'''
t: time
s: autocorrelation
'''
def find_period(t, s):
    popt, pcov = curve_fit(sine, t, s)
    return popt[0]*math.pi