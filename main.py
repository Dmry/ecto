import sys
import pathlib
import logging
import argparse
from math import ceil

import numpy as np

from reader import read
from figures import envelope
from input import Signal

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help = "CSV file to read as input")
parser.add_argument('envelope_time', type=float, help = "Envelope time for given input file")
parser.add_argument("-d", "--debug", action="store_true", help="Set the log level to debug")
parser.add_argument("-o", "--output", help="Set the directory to store output in", default="output")
args = parser.parse_args()

loglevel = logging.INFO if not args.debug else logging.DEBUG
logging.basicConfig(level=loglevel)

if not len(sys.argv) > 1:
    parser.print_help()
    exit()

output_dir = pathlib.Path(args.output)
output_dir.mkdir(parents=True, exist_ok=True)

envelope_time = args.envelope_time

logging.info("Reading input file")

df = read(args.input_file)

# Time in miliseconds (0.001 seconds)
time = 0.0001*df.time.to_numpy()

# Get power
# Channel A: high voltage over reactor. Turn down ratio 1000:1.
chan_a = Signal(df.chan_a.to_numpy(), time, step_down = 1000)
# Channel C voltage over ohmic resistor (= current in A) with 10:1 step-down
chan_c = Signal(df.chan_c.to_numpy(), time, step_down = 10)

del df

logging.info(f'Power is: {chan_a.slice_by_period(1, 17.5) * chan_c.slice_by_period(1, 17.5)}')

logging.info("Done")