#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math

from matplotlib import colors
def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')

def hsv2rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h * 6.)
    f = (h * 6.) - i;
    p, q, t = v * (1. - s), v * (1. - s * f), v * (1. - s * (1. - f));
    i %= 6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def gradient_rgb_bw(v):
    #TODO
    return (v, v, v)


def gradient_rgb_gbr(v):
    #TODO
    r= 0
    g= 1-(v*2)
    b= v*2
    if (v>0.5):
        r = (v-0.5)*2
        g = 0
        b = 1-((v-0.5)*2)
    return (r,g,b)


def gradient_rgb_gbr_full(v):
    g= 0
    b= 1
    r= v*5
    if (v>0.2):
        g = 0
        b = 1 -((v-0.2)*(10/3))
        r = 1
        if (v>0.5):
            g = (v-0.5)*(10/3)
            b = 0
            r = 1
            if (v>0.8):
                g = 1
                b = 0
                r = 1 - ((v-0.8)*5)
    return (g, b, r)


def gradient_rgb_wb_custom(v):
    #TODO
    r = 1
    g = 1 - v*7
    b = 1
    if (v > 1/7):
        r = 1 - ((v-1/7)*7)
        g = 0
        b = 1
        if (v > 2/7):
            r = 0
            g = ((v-2/7)*7)
            b = 1
            if (v > 3/7):
                r = 0
                g = 1
                b = 1 - ((v-3/7)*7)
                if (v > 4/7):
                    r = ((v-4/7)*7)
                    g = 1
                    b = 0
                    if (v > 5/7):
                        r = 1
                        g = 1- ((v-5/7)*7)
                        b = 0
                        if (v > 6/7):
                            r = 1 - ((v-6/7)*7)
                            g = 0
                            b = 0
    return (r, g, b)


def gradient_hsv_bw(v):
    #TODO
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    #TODO
    h = (120/360)+v*(239/360)
    return hsv2rgb(h, 1, 1)

def gradient_hsv_unknown(v):
    #TODO
    h = (120 / 360) - v * (120 / 360)
    return hsv2rgb(h, 0.6, 1)


def gradient_hsv_custom(v):
    #TODO
    h = math.sin(v)+(math.cos(v)/2)
    v = math.cos(h)+0.1
    return hsv2rgb(h, 0.7, v)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])

