#!/usr/bin/env python

import sys
# import stats
# import json
import os.path
import Image


windows = [
  # {'type': 'dense', 'size': [3,3]},
  # {'type': 'sparse', 'size': [3,3]},
  # {'type': 'dense', 'size': [4,4]},
  # {'type': 'dense', 'size': [5,5]},
  # {'type': 'sparse', 'size': [5,5]},
  # {'type': 'dense', 'size': [6,6]},
  # {'type': 'dense', 'size': [7,7]},
  # {'type': 'dense', 'size': [8,8]},
  # {'type': 'sparse', 'size': [7,7]},
  {'type': 'sparse', 'size': [9,9]},
  {'type': 'sparse', 'size': [11,11]}
]

# training_set_sizes = ["10", "20", "30", "40", "50"]
training_set_sizes = ["50"]

regions = ["TextRegion_heading", "TextRegion_paragraph"]

test_imgsets = {
  "cacm": [689, 692, 695, 802, 803],
  "time": [783, 784, 785, 786]
}

experiments_root_dir = "/Users/rcillo/tcc/experiment_result"

def result_base_path(image, pub, window, training_set_size, region):
  return experiments_root_dir + '/output/' + pub + '/' + region + '/' + training_set_size + '_percent/' + window['type'] + '/' + str(window['size'][0]) + 'x' + str(window['size'][1]) + '/' + str(image)

def ideal_path(image, pub, region):
  return experiments_root_dir + '/imgsets/' + pub + '/' + str(image) + '_' + region + '.pgm'

def original_path(image, pub):
  return experiments_root_dir + '/imgsets/' + pub + '/' + str(image) + '_black_and_white.pgm'

def result_path(image, pub, window, training_set_size, region):
  return result_base_path(image, pub, window, training_set_size, region) + '.pgm'

def consensus_path(image, pub, window, training_set_size, region):
  return result_base_path(image, pub, window, training_set_size, region) + '_consensus.pgm'

def exists_consensus(image, pub, window, tsize):
  return os.path.exists(consensus_path(image, pub, window, tsize, "TextRegion_paragraph")) and os.path.exists(consensus_path(image, pub, window, tsize, "TextRegion_heading"))

def merged_path(image, pub, window, tsize):
  return experiments_root_dir + '/merged/' + pub + '_' + tsize + '_percent_' + window['type'] + '_' + str(window['size'][0]) + 'x' + str(window['size'][1]) + '_' + str(image) + '_final.png'

def merged_ideal_path(pub, image):
  return experiments_root_dir + '/final_ideal/' + pub +  '_' + str(image) + '_ideal.png'
  

def merge(paragraph_consensus, heading_consensus, original):
  paragraph = paragraph_consensus.load()
  heading = heading_consensus.load()
  original_pixels = original.load()
  merged = Image.new("RGB", original.size, "white")
  merged_pixels = merged.load()
  cyan = (0, 0, 255)
  magenta = (255, 0, 0)
  green = (0, 255, 0)
  black = (0, 0, 0)
  yellow = (255, 255, 0)
  for row in xrange(0, original.size[0]):
    for col in xrange(0, original.size[1]):
      if paragraph[row, col] == 0:
        merged_pixels[row, col] = cyan
      elif heading[row, col] == 0:
        merged_pixels[row, col] = green
      elif original_pixels[row, col] == 0:
        merged_pixels[row, col] = magenta
  return merged

def ideal(original, pub, image):
  paragraph = Image.open(ideal_path(image, pub, "TextRegion_paragraph")).convert("1").load()
  heading = Image.open(ideal_path(image, pub, "TextRegion_heading")).convert("1").load()
  original_pixels = original.load()
  ideal = Image.new("RGB", original.size, "white")
  ideal_pixels = ideal.load()
  cyan = (0, 0, 255)
  magenta = (255, 0, 0)
  green = (0, 255, 0)
  black = (0, 0, 0)
  yellow = (255, 255, 0)
  for row in xrange(0, original.size[0]):
    for col in xrange(0, original.size[1]):
      if original_pixels[row, col] == 0:
        if paragraph[row, col] == 255:
          ideal_pixels[row, col] = cyan
        elif heading[row,col] == 255:
          ideal_pixels[row, col] = green
        else:
          ideal_pixels[row, col] = magenta
  return ideal

for pub in test_imgsets.keys():
  for image in test_imgsets[pub]:
    original_image_path = original_path(image, pub)
    original = Image.open(original_image_path).convert("1")
    if not os.path.exists(merged_ideal_path(pub, image)):
      ideal(original, pub, image).save(merged_ideal_path(pub, image))
    for window in windows:
        for tsize in training_set_sizes:
          if exists_consensus(image, pub, window, tsize) and not os.path.exists(merged_path(image, pub, window, tsize)):
            paragraph_consensus_path = consensus_path(image, pub, window, tsize, "TextRegion_paragraph")
            paragraph_consensus = Image.open(paragraph_consensus_path).convert("1")
            heading_consensus_path = consensus_path(image, pub, window, tsize, "TextRegion_heading")
            heading_consensus = Image.open(heading_consensus_path).convert("1")
            merged = merge(paragraph_consensus, heading_consensus, original)
            merged.save(merged_path(image, pub, window, tsize))
