# Using the magic encoding
# -*- coding: utf-8 -*-

import numpy as np
from pylab import figure, show
import matplotlib.image as mpimg
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.font_manager as fm

def original_histogram():
    img = mpimg.imread('h_3grayscale.png')

    fig = figure()
    ax = fig.add_subplot(111)

    # ajusta o range de níveis de cinza para ir de 0 a 255
    g = np.vectorize(lambda x: x * 255.0 / img.max())
    N, bins, patches = ax.hist(g(img.flatten()), 8)

    # fp1=fm.FontProperties(fname="/Users/rcillo/Documents/bcc/tcc/monografia/assets/fonts/HelveticaNeueUltraLight.ttf", size='x-large')
    # ax.set_xlabel(u'Níveis de cinza', fontproperties=fp1)
    # ax.set_ylabel(u'Frequência', fontproperties=fp1)

    # ax.set_xlabel(u'Níveis de cinza')
    # ax.set_ylabel(u'Frequência')

    ax.axis([0, 255, 0, N.max()])

    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    n = len(patches)

    # pinta as barras nos seus respectivos níveis de cinza
    for thispatch, idx in zip(patches, range(1, n+1)):
        gray = (idx * 1.0) / (n * 1.0)
        thispatch.set_facecolor([gray, gray, gray, 1.0])


    # show()
    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*0.2, DefaultSize[1]*0.2) )

    canvas = FigureCanvasAgg(fig)
    
    canvas.print_figure("3bit_hist.png", dpi=80)

def thresholded_histogram(threshold):

    filename = "h_3grayscale.png"
    img = mpimg.imread(filename)

    fig = figure()
    ax = fig.add_subplot(111)

    # ajusta o range de níveis de cinza para ir de 0 a 255
    g = np.vectorize(lambda x: round(x * 255.0 / img.max()))
    N, bins, patches = ax.hist(g(img.flatten()), 8)

    t = round((threshold * 1.0) / 100.0 * 255.0 / 34.0)
    l = len(img.flatten())
    wb = 0
    wf = 0
    n = img.flatten().size
    for x in g(img.flatten()):
      if x <= round((threshold * 1.0) / 100.0 * 255.0):
        wb += 1
      else:
        wf += 1

    mf = 0
    mb = 0
    for x in g(img.flatten()):
      if x <= round((threshold * 1.0) / 100.0 * 255.0):
        mb += x / wb
      else:
        mf += x / wf

    pwb = wb * 1.0 / l * 1.0
    pwf = wf * 1.0 / l * 1.0

    vb = 0
    vf = 0
    for x in g(img.flatten()):
      if x <= round((threshold * 1.0) / 100.0 * 255.0):
        vb += (x - mb) * (x - mb) / wb
      else:
        vf += (x - mf) * (x - mf) / wf

    vw = wb * vb * vb + wf * vf * vf

    print "threshold: ", threshold, "t: ", t, "x: ", round((threshold * 1.0) / 100.0 * 255.0), "wb: ", wb, "pwb: ", pwb, "mb: ", mb, "vb: ", vb, "wf: ", wf, "pwf: ", pwf, "mf: ", mf, "vf: ", vf, "vw: ", vw

    # ax.set_xlabel(u'Níveis de cinza')
    # ax.set_ylabel(u'Frequência')

    ax.axis([0, 255, 0, N.max()])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    n = len(patches)

    # pinta as barras nos seus respectivos níveis de cinza
    # l = (threshold / 10.0)
    # print "threshold", threshold
    # print l
    for thispatch, idx in zip(patches, range(1, n+1)):
      if idx <= t:
        thispatch.set_facecolor([0, 0, 0, 1.0])
      else:
        thispatch.set_facecolor([1.0, 1.0, 1.0, 1.0])

    DefaultSize = fig.get_size_inches()
    fig.set_size_inches( (DefaultSize[0]*0.2, DefaultSize[1]*0.2) )
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(str(threshold)+"hist.png", dpi=80)


original_histogram()
thresholded_histogram(13)
thresholded_histogram(25)
thresholded_histogram(38)
thresholded_histogram(50)
thresholded_histogram(63)
thresholded_histogram(75)
thresholded_histogram(88)
