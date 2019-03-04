import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scripts.stuff import checkFilyType, img_to_html, colorPP


plt.rcParams.update({'font.size': 16})


def IDoverRT(ax, df, title, RTcolumn, color, min):
    """ plot the number of Identifications for specified minute interval min , default: 5 min
    datasource: an:  pyprophet or swath, osw or tsv,
    :params df, raw dataframe from any file, RTcolumn: 'RT' for pptsv, or swath tsv, 'EXP_RT' fow pp osw and swath osw
    :return figure formatted as html string"""

    df[RTcolumn] = df.loc[:, RTcolumn].apply(lambda x: x/60)
    # bin RT range
    RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), min)

    xlabs = [min * i for i in range(len(RTrange))]

    # group by time interval and count
    # library patch
    ax.hist(df.loc[:, RTcolumn], bins=RTrange, color=color, edgecolor="k")
    plt.title(title)
    plt.xlabel('RT[min]')
    plt.ylabel('# of IDs')

    plt.xticks(RTrange)

    # style x and y labels:
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(12)
    for label, i in zip(ax.xaxis.get_ticklabels(), xlabs):

         #label is a Text instance
        label.set_rotation(45)
        label.set_fontsize(12)
        #label.set_text(i)

    #xtickNames = plt.setp(ax, xticklabels=RTrange)
    #plt.setp(xtickNames, fontsize=14)

def plot(dfdict, filedict, min=5, cols=2):
    """ plot multiple subfigures
        plot the number of Identifications for specified minute interval min , default: 5 min
        datasource: this can be plotted from any file: pyprophet or swath, osw or tsv,
        :params df, raw dataframe from any file, RTcolumn: 'RT' for pptsv, or swath tsv, 'EXP_RT' fow pp osw and swath osw
        :return figure formatted as html string"""
    # get dataframe length and keys
    keys = dfdict.keys()
    N = len(dfdict)
    keyindex = zip(range(N), keys)
    # set up grid
    rows = int(math.ceil(N / cols))
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(24, 7*rows))
    # Todo: shared y axis between all subplots

    # plot each dataframe in dict

    for n, key in keyindex:
        color = colorPP(key, filedict)
        filetype = checkFilyType(key)
        if filetype == 'osw':
            RTcolumn = 'EXP_RT'
        if filetype == 'tsv':
            RTcolumn = 'RT'
        # set ax
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        IDoverRT(ax, df, key, RTcolumn, color, min)
    fig.subplots_adjust(hspace=.3, wspace=.001)

    plt.suptitle('ID over RT')


    def describe(keys, minutes=5):
        """return html string"""
        html = "This histogram shows the number of feature identified in a specified retention time interval. In this plot, each " \
               "bar represents a {} minute interval, the actual retention time is displayed in seconds on the x axis.<br>" \
               "These plots can be generated from any OpenSwathWorkflow or pyprophet output files, that can be either in either in tsv or osw fromat" \
               "For each given input file a subplot is generated.<br> Please compare runs and make sure, " \
               "the number of IDs are stable over RT dimension and between runs. <br>Files used to create plots: <ul><li>".format(minutes)
        html += "</li><li>".join(k for k in list(keys))
        html += "</ul>"
        return html

    return (img_to_html(fig), describe(keys), 'IDoverRT')