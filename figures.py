import matplotlib.pyplot as plt
import numpy as np
import pathlib
from numpy.fft import fft, ifft, ifftshift
from math import ceil

def all(t, s, folder="output"):
    pathlib.Path('output').mkdir(parents=True, exist_ok=True)
    #print("signal")
    #signal(t, s)
    print("autocorrelation")
    autocorr(t, s)
    print("magnitude")
    magnitude_spectrum(t, s)
    print("log_magnitude")
    log_magnitude_spectrum(t, s)
    print("phase_spectrum")
    phase_spectrum(t, s)
    print("angle_spectrum")
    angle_spectrum(t, s)

def signal(t, s, folder="output"):
    plt.scatter(t, s, color='C0')
    plt.title("Signal")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig(f'{folder}/signal.png')
    plt.clf()

def autocorr(t,x, folder="output"):
    xp = ifftshift((x - np.average(x))/np.std(x))
    n, = xp.shape
    xp = np.r_[xp[:n//2], np.zeros_like(xp), xp[n//2:]]
    f = fft(xp)
    del xp
    p = np.absolute(f)**2
    del f
    pi = ifft(p)
    del p
    s = np.real(pi)[:n//2]/(np.arange(n//2)[::-1]+n//2)
    plt.plot(t[0:len(s)],s)
    plt.title("Autocorrelation")
    plt.savefig(f'{folder}/autocorrelation.png')
    plt.clf()

def magnitude_spectrum(t, s, folder="output"):
    dt = t[1]
    Fs = 1 / dt
    plt.magnitude_spectrum(s, Fs=Fs, color='C1')
    plt.title("Magnitude Spectrum")
    plt.savefig(f'{folder}/magnitude.png')
    plt.clf()

def log_magnitude_spectrum(t, s, folder="output"):
    dt = t[1]
    Fs = 1 / dt
    plt.magnitude_spectrum(s, Fs=Fs, scale='dB', color='C1')
    plt.title("Log. Magnitude Spectrum")
    plt.savefig(f'{folder}/log_magnitude.png')
    plt.clf()

def phase_spectrum(t, s, folder="output"):
    dt = t[1]
    Fs = 1 / dt
    plt.phase_spectrum(s, Fs=Fs, color='C1')
    plt.title("Phase Spectrum")
    plt.savefig(f'{folder}/phase.png')
    plt.clf()

def angle_spectrum(t, s, folder="output"):
    dt = t[1]
    Fs = 1 / dt
    plt.angle_spectrum(s, Fs=Fs, color='C1')
    plt.title("Phase Spectrum")
    plt.savefig(f'{folder}/angle.png')
    plt.clf()