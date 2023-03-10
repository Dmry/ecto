import logging
import math

import numpy as np
import cupy as cp
from scipy.optimize import curve_fit
from numpy.fft import ifftshift

class Signal:
    def __init__(self, value : np.ndarray, time : np.ndarray, step_down = 1):
        self.signal = value
        self.time = time
        self.step_down = step_down

    def autocorrelation(self):
        logging.debug("Shifting")
        xp = ifftshift((self.signal - np.average(self.signal))/np.std(self.signal))
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
    
    def find_period(self):
        def sine(t, p):
            return 0.5*(np.cos((1/p)*t)+1)

        popt, pcov = curve_fit(sine, self.time, self.autocorrelation())
        return popt[0]*math.pi
    
    def slice_by_period(self, index, period_time):
        i = (np.abs(self.time - period_time)).argmin()
        logging.debug(f'Found index {i} for period {period_time}')

        try:
            return self.step_down * self.signal[0:index*i]
        except:
            return None