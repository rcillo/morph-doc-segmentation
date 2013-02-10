#!/usr/bin/env python

import sys
import stats
import json

import matplotlib.pyplot as plt
import numpy as np

windows = [
  {'type': 'dense', 'size': [3,3]},
  {'type': 'sparse', 'size': [3,3]},
  {'type': 'dense', 'size': [4,4]},
  {'type': 'dense', 'size': [5,5]},
  {'type': 'sparse', 'size': [5,5]},
  {'type': 'dense', 'size': [6,6]},
  {'type': 'dense', 'size': [7,7]},
  # {'type': 'dense', 'size': [8,8]},
  {'type': 'sparse', 'size': [7,7]},
  {'type': 'sparse', 'size': [9,9]},
  {'type': 'sparse', 'size': [11,11]}
]

training_set_sizes = ["10", "20", "30", "40", "50"]

regions = ["TextRegion_heading", "TextRegion_paragraph"]

experiments_root_dir = "/Users/rcillo/tcc/experiment_result"

plot_dir = experiments_root_dir + "/charts"

def result_base_path(image, pub, window, training_set_size, region):
  return experiments_root_dir + '/output/' + pub + '/' + region + '/' + training_set_size + '_percent/' + window['type'] + '/' + str(window['size'][0]) + 'x' + str(window['size'][1]) + '/' + str(image)

def ideal_path(image, pub, window, training_set_size, region):
  return experiments_root_dir + '/imgsets/' + pub + '/' + str(image) + '_' + region + '.pgm'

def original_path(image, pub, window, training_set_size, region):
  return experiments_root_dir + '/imgsets/' + pub + '/' + str(image) + '_black_and_white.pgm'

def result_path(image, pub, window, training_set_size, region):
  return result_base_path(image, pub, window, training_set_size, region) + '.pgm'

pub = sys.argv[2]
image = sys.argv[3]
for window in windows:
  