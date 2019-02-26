#!/usr/bin/env python

"""Functions to plot a bargraph
-
"""
from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt


def barplot(df, title, ylabel, xlabel, figsize=(12, 7), color='coral', titlefontsize=14, labelcolor='dimgrey'):
    """
    draw barplot for preprocessed dataframe,
    :param processed dataframe, ready to plot, add title, ylabl and xlabel
    :return: figure
    """
    # draw plot
    ax = df.plot(kind='bar', figsize=figsize, color=color, fontsize=14)
    ax.set_alpha(0.8)
    ax.set_title(title, fontsize=titlefontsize)
    ax.set_ylabel(ylabel, fontsize=13)
    ax.set_xlabel(xlabel, fontsize=13)
    ax.xaxis.set_tick_params(rotation=0)

    # place labels on top of bars
    # create a list to collect the plt.patches data
    totals = []
    # find the values and append to list
    for i in ax.patches:
        totals.append(i.get_height())
    # set individual bar lables using above list
    ax.legend()  # need the column to have a sensible name
    # set individual bar lables using above list
    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x(),  i.get_height() + 30, str(i.get_height()), fontsize=12, color=labelcolor)
    fig = ax.get_figure()
    # fig.savefig('test.png', bbox_inches=0.2, frameon=True)
    return fig