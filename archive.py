'''
Get band cutoff
cutoff = df.chan_c.abs().min()

 Select only values > cutoff and < -cutoff
to_integrate = df[(df.chan_c > cutoff) | (df.chan_c < -cutoff)]
to_integrate = df

logging.info("Calculating autocorrelation")
s = autocorr(time, chan_a)
logging.info("Hilbert Transform")
envelope(time[0:ceil(0.5*len(time))], s)
logging.info("Finding period")
period = find_period(time[0:ceil(0.5*len(time))], s)
del s

all(time[0:ceil(pct*len(time))], chan_a[0:ceil(pct*len(chan_a))])

envelope_starts = starts(power, cutoff)
sums = calc_power(power, envelope_starts)
avg = average(sums)

print("Found envelope starts at time points:")
for start in envelope_starts:
        print(time[start])

print("Power averaged over envelopes:")
print(avg)
print("Power of individual envelopes:")
print(sums)
'''