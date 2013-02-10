import Image
import math
from collections import defaultdict

class Stats:

  def file_stats(self, original_image_path, ideal_image_path, result_image_path):
    original_image = Image.open(original_image_path).convert("1")
    ideal_image = Image.open(ideal_image_path).convert("1")
    result_image = Image.open(result_image_path).convert("1")
    return self.image_stats(original_image, ideal_image, result_image)

  def image_stats(self, original_image, ideal_image, result_image):
    original_pixels = original_image.load()
    ideal_pixels = ideal_image.load()
    result_pixels = result_image.load()

    rows, cols = original_image.size

    total_pixels = rows * cols

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for row in xrange(0, rows):
      for col in xrange(0, cols):
        o = original_pixels[row, col]
        i = ideal_pixels[row, col]
        r = result_pixels[row,col]
        if o == 0: # we only measure on turned on pixels
          if i == 255:
            if r == 255:
              tp += 1 # erased (classified) correctly
            else:
              fn += 1 # should had erased but did not
          else:
            if r == 255:
              fp += 1 # should not had erased
            else:
              tn += 1 # did not erased correctly

    stat = defaultdict()
    stat["tp"] = tp
    stat["tn"] = tn
    stat["fp"] = fp
    stat["fn"] = fn

    tp = tp * 1.0
    tn = tn * 1.0
    fp = fp * 1.0
    fn = fn * 1.0

    # http://en.wikipedia.org/wiki/F1_score
    precision = 0
    if tp + fp > 0:
        precision = tp / (tp + fp)
    recall_or_sensitivity = 0
    if tp + fn > 0:
        recall_or_sensitivity = tp / (tp + fn)
    f1 = 0
    if precision + recall_or_sensitivity > 0:
        f1 = 2 * precision * recall_or_sensitivity / (precision + recall_or_sensitivity)

    stat["precision"] = precision
    stat["recall_or_sensitivity"] = recall_or_sensitivity
    stat["f1"] = f1

    # http://en.wikipedia.org/wiki/Matthews_correlation_coefficient
    n = tp + tn + fp + fn
    s = (tp + fn) / n
    p = (tp + fp) / n
    mcc = 0
    if p * s * (1 - s) * (1 - p) > 0:
        mcc = ((tp/n) - s * p) / math.sqrt(p * s * (1 - s) * (1 - p))

    stat["n"] = n
    stat["s"] = s
    stat["p"] = p
    stat["mcc"] = mcc

    return stat
