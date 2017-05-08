#!/usr/bin/env python3

import numpy as np
import argparse
import json
from matplotlib import pyplot as plt

# loads JSON file. Returns plot labels, converted X and Y values.
def load_json(jsonfile):
  json_dir = json.load(open(jsonfile, 'r'))

  names = json_dir['data'].keys()
  data_strs = json_dir['data'].values()

  X_nums = map(lambda x: convert_units(x, json_dir['X1'], json_dir['X2'], 
                                          axis=0), data_strs)
  Y_nums = map(lambda x: convert_units(x, json_dir['Y1'], json_dir['Y2'], 
                                          axis=1), data_strs)
  X_nums = np.array(list(X_nums))
  Y_nums = np.array(list(Y_nums))

  return names, X_nums, Y_nums

# Parses a path string and returns numerical values in canvas/layer
# coordinates.
def parse_path(path):
  if path[0:2] == 'm ' or path[0:2] == 'M ':
    path = path[2:]
  pairs = path.split(' ')

  pairs = [np.array(list(map(float, pair.split(',')))) for pair in pairs]
  for i in range(1, len(pairs)):
    pairs[i] += pairs[i-1]

  return np.array(pairs)

# Computes reference point and step size in both coordinates.
def get_Y_refs(Y1, Y2):
  Y1 = np.array(list(map(float, Y1.split(','))))
  Y2 = np.array(list(map(float, Y2.split(','))))

  diff = Y2 - Y1

  return Y1, diff

# Converts a path string given to reference points. Axis lets you choose
# between X and Y coordinates.
def convert_units(path, ref1, ref2, axis=0):
  pairs = parse_path(path)
  ref, diff = get_Y_refs(ref1, ref2)

  s = (pairs[:,axis] - ref[1]) / diff[1]
  return ref[0] + s * diff[0]

parser = argparse.ArgumentParser(description="Convert SVG path of plots to "
                                             "numerical values.")
parser.add_argument("json", type=str,
                    help="JSON file.")
parser.add_argument("-o", "--outfile", type=str,
                    help="JSON output file.")
parser.add_argument("-q", "--quiet", action='store_true',
                    help="Disalbe plot and console output.")

args=parser.parse_args()  

# Load data from json
names, Xs, Ys = load_json(args.json)

converted_data = {}
for name, x, y in zip(names, Xs, Ys):
  # Directory for JSON output file.
  converted_data[name] = [x.tolist(), y.tolist()]
  if not args.quiet:
    print("---------- {}\nX = {}\nY = {}".format(name, x, y))
    # Test plot.
    plt.plot(x, y, label=name)

# Write output.
if args.outfile:
  json.dump(converted_data, open(args.outfile, 'w'))

if not args.quiet:
  plt.legend()
  plt.show()
