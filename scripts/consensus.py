#!/usr/bin/env python

import sys
# import stats
# import json
import os.path

import Image

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

test_imgsets = {
  "cacm": [689, 692, 695, 802, 803],
  "time": [783, 784, 785, 786]
}

experiments_root_dir = "/Users/rcillo/tcc/experiment_result"

def result_base_path(image, pub, window, training_set_size, region):
  return experiments_root_dir + '/output/' + pub + '/' + region + '/' + training_set_size + '_percent/' + window['type'] + '/' + str(window['size'][0]) + 'x' + str(window['size'][1]) + '/' + str(image)

def ideal_path(image, pub, window, training_set_size, region):
  return experiments_root_dir + '/imgsets/' + pub + '/' + str(image) + '_' + region + '.pgm'

def original_path(image, pub):
  return experiments_root_dir + '/imgsets/' + pub + '/' + str(image) + '_black_and_white.pgm'

def result_path(image, pub, window, training_set_size, region):
  return result_base_path(image, pub, window, training_set_size, region) + '.pgm'

def consensus_path(image, pub, window, training_set_size, region):
  return result_base_path(image, pub, window, training_set_size, region) + '_consensus.pgm'

def exists_consensus(image, pub, window, tsize):
  return os.path.exists(consensus_path(image, pub, window, tsize, "TextRegion_paragraph")) and os.path.exists(consensus_path(image, pub, window, tsize, "TextRegion_heading"))

def count(original, region_input, row, col, win_size):
  original_pixels = original.load()
  total = 0
  for i in xrange(max(0, row - win_size[0]/2), min(original.size[0], row + win_size[0]/2)):
    for j in xrange(max(0, col - win_size[1]/2), min(original.size[1], col + win_size[1]/2)):
      if original_pixels[i, j] == 0 and region_input[i,j] == 255:
        total += 1
  return total

def count_total(original, row, col, win_size):
  original_pixels = original.load()
  total = 0
  for i in xrange(max(0, row - win_size[0]/2), min(original.size[0], row + win_size[0]/2)):
    for j in xrange(max(0, col - win_size[1]/2), min(original.size[1], col + win_size[1]/2)):
      if original_pixels[i, j] == 0:
        total += 1
  return total

def consensus_for_window(row, col, win_size, original, paragraph_input, heading_input):
  original_pixels = original.load()
  if original_pixels[row, col] == 0:
    if paragraph_input[row,col] == 255 and heading_input[row, col] == 0:
      return "TextRegion_paragraph"
    elif paragraph_input[row,col] == 0 and heading_input[row, col] == 255:
      return "TextRegion_heading"
    elif paragraph_input[row,col] == 0 and heading_input[row, col] == 0:
      paragraphs = count(original, paragraph_input, row, col, win_size)
      headings = count(original, heading_input, row, col, win_size)
      total = count_total(original, row, col, win_size)
      if paragraphs > total * 1.0 / 2.0 and paragraphs > headings:
        return "TextRegion_paragraph"
      elif headings > total * 1.0 / 2.0 and headings > paragraphs:
        return "TextRegion_heading"
    return None

def compute_consensus(original, paragraph_input, heading_input, image, pub, tsize, window):
  rows, cols = original.size
  new_paragraph_path = consensus_path(image, pub, window, tsize, "TextRegion_paragraph")
  new_heading_path = consensus_path(image, pub, window, tsize, "TextRegion_heading")
  new_images = {
    "TextRegion_paragraph": Image.new("1", original.size, "white"),
    "TextRegion_heading": Image.new("1", original.size, "white")
  }
  pixels = {
    "TextRegion_paragraph": new_images["TextRegion_paragraph"].load(),
    "TextRegion_heading": new_images["TextRegion_heading"].load()
  }
  for row in xrange(0, rows):
    for col in xrange(0, cols):
      consensus_region = consensus_for_window(row, col, [9,9], original, paragraph_input.load(), heading_input.load())
      if consensus_region != None:
        pixels[consensus_region][row, col] = 0
  new_images["TextRegion_paragraph"].save(new_paragraph_path)
  new_images["TextRegion_heading"].save(new_heading_path)

if sys.argv[1] = "generate"
  pub = sys.argv[2]
  image = sys.argv[3]
  original_image_path = original_path(image, pub)
  original = Image.open(original_image_path).convert("1")
  for window in windows:
    for tsize in training_set_sizes:
      if not exists_consensus(image, pub, window, tsize):
        paragraph_input_path = result_path(image, pub, window, tsize, "TextRegion_paragraph")
        paragraph_input = Image.open(paragraph_input_path).convert("1")
        heading_input_path = result_path(image, pub, window, tsize, "TextRegion_heading")
        heading_input = Image.open(heading_input_path).convert("1")
        compute_consensus(original, paragraph_input, heading_input, image, pub, tsize, window)

def measure():
  for pub in test_imgsets.keys():
    for window in windows:
      for region in regions:
        for training_set_size in training_set_sizes:
          for image_number in test_imgsets[pub]:
            original_image_path = original_path(image_number, pub, window, training_set_size, region)
            ideal_image_path = ideal_path(image_number, pub, window, training_set_size, region)
            result_image_path = consensus_path(image_number, pub, window, training_set_size, region)
            stat_json_path = stat_consensus_path(image_number, pub, window, training_set_size, region)
            stat = stats.Stats().file_stats(original_image_path, ideal_image_path, result_image_path)
            f = open(stat_json_path, 'w')
            f.write(json.dumps(stat))
            f.close()
            print stat_json_path

if sys.argv[1] = "measure"
  measure()  

