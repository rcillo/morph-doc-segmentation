#!/usr/bin/env python

import sys
import stats
import json

import matplotlib.pyplot as plt
import numpy as np

test_imgsets = {
  "cacm": [689, 692, 695, 802, 803],
  "time": [783, 784, 785, 786]
}

quantity = {
  "cacm": {
    "10": "2",
    "20": "3",
    "30": "4",
    "40": "5",
    "50": "7",
  }
}

metrics = ['precision', 'recall_or_sensitivity', 'f1', 'mcc']

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

translations = {
  'precision': 'Precision',
  'recall_or_sensitivity': 'Recall',
  'f1': 'F-measure',
  'mcc': 'MCC'
}

regions = ["TextRegion_heading", "TextRegion_paragraph"]

training_set_sizes = ["10", "20", "30", "40", "50"]

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

def stat_path(image, pub, window, training_set_size, region):
  return result_base_path(image, pub, window, training_set_size, region) + '.json'

def load_stat(image_number, pub, window, training_set_size, region):
  stat_json_path = stat_path(image_number, pub, window, training_set_size, region)
  f = open(stat_json_path, 'r')
  stat = json.load(f)
  f.close()
  return stat

def load_stats():
  stats = []
  for pub in test_imgsets.keys():
    for window in windows:
      for region in regions:
        for training_set_size in training_set_sizes:
          for image_number in test_imgsets[pub]:
            stat = load_stat(image_number, pub, window, training_set_size, region)
            stats.append(stat)
            stat["pub"] = pub
            stat["window"] = window
            stat["training_set_size"] = training_set_size
            stat["image"] = image_number
            stat["region"] = region
  return stats

            
def generate():
  for pub in test_imgsets.keys():
    for window in windows:
      for region in regions:
        for training_set_size in training_set_sizes:
          for image_number in test_imgsets[pub]:
            original_image_path = original_path(image_number, pub, window, training_set_size, region)
            ideal_image_path = ideal_path(image_number, pub, window, training_set_size, region)
            result_image_path = result_path(image_number, pub, window, training_set_size, region)
            stat_json_path = stat_path(image_number, pub, window, training_set_size, region)
            stat = stats.Stats().file_stats(original_image_path, ideal_image_path, result_image_path)
            f = open(stat_json_path, 'w')
            f.write(json.dumps(stat))
            f.close()
            print stat_json_path

if sys.argv[1] == "generate":
  generate()

def mean(pub, window, tsize, region, stat_key):
  pub_images = test_imgsets[pub]
  number_of_images = len(pub_images) * 1.0
  m = 0.0
  for image_number in pub_images:
    stat = load_stat(image_number, pub, window, tsize, region)
    m += stat[stat_key] / number_of_images
  return m

# \begin{center}
#   \begin{tabular}{ l | l l l l l || l l l l l | }
#     \cline{2-11}
#     & \multicolumn{10}{|c|}{janelas} \\
#     \cline{2-11}
#     & \multicolumn{5}{c||}{densa} & \multicolumn{5}{c|}{esparsa} \\
#     \cline{2-11}
#     & 3x3 & 4x4 & 5x5 & 6x6 & 7x7 & 3x3 & 5x5 & 7x7 & 9x9 & 11x11 \\
#     \hline
#     \multicolumn{1}{|l|}{10\%} & 3 & 4 & 5 & 6 & 7 & 3 & 5 & 7 & 9 & 11 \\
#     \multicolumn{1}{|l|}{20\%} & 3 & 4 & 5 & 6 & 7 & 3 & 5 & 7 & 9 & 11 \\
#     \multicolumn{1}{|l|}{30\%} & 3 & 4 & 5 & 6 & 7 & 3 & 5 & 7 & 9 & 11 \\
#     \multicolumn{1}{|l|}{40\%} & 3 & 4 & 5 & 6 & 7 & 3 & 5 & 7 & 9 & 11 \\
#     \multicolumn{1}{|l|}{50\%} & 3 & 4 & 5 & 6 & 7 & 3 & 5 & 7 & 9 & 11 \\
#     \hline  
#   \end{tabular}
# \end{center}
if sys.argv[1] == "gen_table":
  pub = sys.argv[2] # cacm
  region = sys.argv[3] # "TextRegion_paragraph"
  stat_key = sys.argv[4] # 'f1'
  for tsize in training_set_sizes:
    sys.stdout.write('\\multicolumn{1}{|l|}{' + tsize + '\\%}')
    for window in windows:
      m = mean(pub, window, tsize, region, stat_key)
      sys.stdout.write('& ' + str("%.4f" % m))
    sys.stdout.write('\\\\\n')

# var data = google.visualization.arrayToDataTable([
#           ['Year', 'Sales', 'Expenses'],
#           ['2004',  1000,      400],
#           ['2005',  1170,      460],
#           ['2006',  660,       1120],
#           ['2007',  1030,      540]
#         ]);
if sys.argv[1] == "gen_chart":
  pub = sys.argv[2] # cacm
  region = sys.argv[3] # "TextRegion_paragraph"
  stat_key = sys.argv[4] # 'f1'
  sys.stdout.write("['Janela'")
  for tsize in training_set_sizes:
    # sys.stdout.write(", '" + quantity[pub][tsize] + " imagens'")
    sys.stdout.write(", '" + tsize + "%'")
  sys.stdout.write("],\n")
  for window in windows:
    sys.stdout.write("['"+str(window['size'][0])+"x"+str(window['size'][1])+" "+window['type']+"'")
    for tsize in training_set_sizes:
      m = mean(pub, window, tsize, region, stat_key)
      sys.stdout.write(', ' + str("%.4f" % m))
    sys.stdout.write('],\n')

def plot_bars(groups, group_labels, legends, ylabel, yscale=None):
  N = len(group_labels)

  ind = np.arange(N)  # the x locations for the groups
  width = 0.1       # the width of the bars

  plt.rc('xtick', labelsize=12) 
  plt.rc('ytick', labelsize=12) 
  fig = plt.figure(figsize=(14,7), dpi=300)
  ax = fig.add_subplot(111)

  colors = ['b', 'r', 'y', 'g', 'm']

  rects = []
  i = 0
  for group in groups:
    rects.append(ax.bar(ind + ((i + 3) * 1.0 * width), group, width, bottom=10**-3, color=colors[i]))
    i += 1
  
  ax.set_xticks(ind+0.5+width)
  ax.set_xticklabels( group_labels )

  box = ax.get_position()
  ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
  ax.legend(rects, legends, loc='center left', bbox_to_anchor=(1, 0.5), prop={'size':14})

  if yscale != None:
    plt.yscale(yscale)

  plt.ylabel(ylabel, fontsize=14)
  return plt

def window_name(window):
  return str(window['size'][0]) + "x" + str(window['size'][1])

def plot(pub, region, stat_key):
  groups = []
  for tsize in training_set_sizes:
    group = []
    for window in windows:
      m = mean(pub, window, tsize, region, stat_key)
      group.append(m)
    groups.append(group)
  
  group_labels = []
  for window in windows:
    group_labels.append(str(window['size'][0])+"x"+str(window['size'][1])+" "+window['type'])

  legends = []
  for tsize in training_set_sizes:
    legends.append(tsize+'%')

  plt = plot_bars(groups, group_labels, legends, translations[stat_key])
  if(stat_key == 'mcc'):
    plt.ylim([-1.0,1.0])
  else:
    plt.ylim([0,1.0])
  # plt.show()
  plt.savefig(plot_dir + "/" + pub + "_" + region + "_" + stat_key + ".png")

if sys.argv[1] == "charts":
  for pub in test_imgsets.keys():
    for region in regions:
      for stat_key in metrics:
        plot(pub, region, stat_key)

if sys.argv[1] == "time_chart":
  times = {
    "TextRegion_heading": {
      "10": {
        "dense": {
          "3x3": 7.9,
          "4x4": 10.8,
          "5x5": 26.4,
          "6x6": 131.3,
          "7x7": 523.2
        },
        "sparse": {
          "3x3": 4.9,
          "5x5": 7.4,
          "7x7": 18.3,
          "9x9": 54.1,
          "11x11": 1238.1
        }
      },
      "20": {
        "dense": {
          "3x3": 11.4,
          "4x4": 15.5,
          "5x5": 30.2,
          "6x6": 286.2,
          "7x7": 2560.4
        },
        "sparse": {
          "3x3": 7.5,
          "5x5": 11.0,
          "7x7": 35.3,
          "9x9": 58.3,
          "11x11": 2415.5
        }
      },
      "30": {
        "dense": {
          "3x3": 15.0,
          "4x4": 20.2,
          "5x5": 37.5,
          "6x6": 259.6,
          "7x7": 1132.37
        },
        "sparse": {
          "3x3": 10.0,
          "5x5": 14.6,
          "7x7": 50.6,
          "9x9": 82.5,
          "11x11": 3272.9
        }
      },
      "40": {
        "dense": {
          "3x3": 18.6,
          "4x4": 24.8,
          "5x5": 47.8,
          "6x6": 412.9,
          "7x7": 3237.6
        },
        "sparse": {
          "3x3": 12.6,
          "5x5": 18.0,
          "7x7": 58.0,
          "9x9": 121.1,
          "11x11": 3298.6
        }
      },
      "50": {
        "dense": {
          "3x3": 26.3,
          "4x4": 35.3,
          "5x5": 61.8,
          "6x6": 344.5,
          "7x7": 4202.8
        },
        "sparse": {
          "3x3": 17.5,
          "5x5": 25.5,
          "7x7": 72.63,
          "9x9": 132.0,
          "11x11": 4432.9
        }
      }
    },
    "TextRegion_paragraph": {
      "10": {
        "dense": {
          "3x3": 7.7,
          "4x4": 12.3,
          "5x5": 55.2,
          "6x6": 437.2,
          "7x7": 3414.1
        },
        "sparse": {
          "3x3": 4.9,
          "5x5": 7.4,
          "7x7": 13.9,
          "9x9": 77.9,
          "11x11": 942.5
        }
      },
      "20": {
        "dense": {
          "3x3": 11.4,
          "4x4": 25.7,
          "5x5": 79.3,
          "6x6": 1024.6,
          "7x7": 19471.3
        },
        "sparse": {
          "3x3": 7.5,
          "5x5": 11.1,
          "7x7": 29.3,
          "9x9": 92.8,
          "11x11": 3889.8
        }
      },
      "30": {
        "dense": {
          "3x3": 15.1,
          "4x4": 22.7,
          "5x5": 109.5,
          "6x6": 1091.2,
          "7x7": 14366.3
        },
        "sparse": {
          "3x3": 10.0,
          "5x5": 14.7,
          "7x7": 42.1,
          "9x9": 127.6,
          "11x11": 6258.3
        }
      },
      "40": {
        "dense": {
          "3x3": 18.7,
          "4x4": 27.6,
          "5x5": 121.6,
          "6x6": 1216.2,
          "7x7": 24548.0
        },
        "sparse": {
          "3x3": 12.6,
          "5x5": 18.0,
          "7x7": 51.3,
          "9x9": 158.7,
          "11x11": 5749.8
        }
      },
      "50": {
        "dense": {
          "3x3": 26.4,
          "4x4": 38.1,
          "5x5": 148.9,
          "6x6": 1428.9,
          "7x7": 34084.0
        },
        "sparse": {
          "3x3": 17.5,
          "5x5": 25.5,
          "7x7": 62.5,
          "9x9": 185.1,
          "11x11": 7453.8
        }
      }
    }
  }
  for region in regions:
    groups = []
    for tsize in training_set_sizes:
      group = []
      for window in windows:
        time = times[region][tsize][window['type']][window_name(window)]
        group.append(time)
      groups.append(group)
    
    group_labels = []
    for window in windows:
      group_labels.append(window_name(window)+" "+window['type'])

    legends = []
    for tsize in training_set_sizes:
      legends.append(tsize+'%')

    plt = plot_bars(groups, group_labels, legends, "Segundos", 'log')
    plt.ylim([0,1000000.0])
    # plt.show()
    plt.savefig(plot_dir + "/" + region + "_time_log.png")

    plt = plot_bars(groups, group_labels, legends, "Segundos")
    plt.ylim([0,1000000.0])
    # plt.show()
    plt.savefig(plot_dir + "/" + region + "_time.png")

