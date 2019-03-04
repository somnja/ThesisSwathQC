''' create plot and description for distribution of peak width over RT
Peak Width is calculated from leftWidth and rightWidth
(or maybe alternatively from fwhm?)'''
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scripts.stuff import checkFilyType, img_to_html, colorPP

plt.rcParams.update({'font.size': 16})


def plot(dfdict, filedict, min=5, cols=1):
    """
    boxplots of Peak Width for given dict of dataframesw, arrange plots deppending on size of dataframe
    determine osw or tsv source from dataframe keys
    :param dfdict: dict of dataframes, either from tsv or osw FEATURE table
    :param min: time interval on RT, default 5 min
    :param cols: number of subplots per column, default: 1
    :return: tuple: (fig as html, description as html, sectionid as string)
    """

    keys = dfdict.keys()
    N = len(dfdict)
    keyindex = zip(range(N), keys)

    rows = int(math.ceil(N / cols))
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 5 * rows))

    for n, key in keyindex:
        filetype = checkFilyType(key)
        # set ax
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]

        #Todo: different color on pp boxplot?
        color=colorPP(key, filedict)

        if filetype == 'tsv':
            RTcolumn = 'RT'
            RWcolumn = 'rightWidth'
            LWcolumn = 'leftWidth'
        if filetype == 'osw':
            RTcolumn = 'EXP_RT'
            RWcolumn = 'RIGHT_WIDTH'
            LWcolumn = 'LEFT_WIDTH'

        RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), 60 * min)
        xlabs = [min * i for i in range(len(RTrange))]
        df_to_plot = df.loc[:, [RWcolumn, LWcolumn, RTcolumn]]
        df_to_plot['widthDiff'] = df_to_plot.loc[:, RWcolumn] - df_to_plot.loc[:, LWcolumn]
        df_to_plot['bin'] = pd.cut(df_to_plot.loc[:, RTcolumn], RTrange)

        df_to_plot.boxplot(column='widthDiff', by='bin', rot=90, grid=False, figsize=(20, 7), ax=ax)
        ax.set_title(key)
        ax.set_xlabel('RT [in {} min intervals]'.format(str(min)))
        ax.set_ylabel('PeakWidth [ppm]')
        xtickNames = plt.setp(ax, xticklabels=xlabs)
        plt.setp(xtickNames, rotation=45, fontsize=14)

    fig.subplots_adjust(hspace=.4, wspace=.01)
    fig.suptitle('PeakWidth over RT')

    def describePWoverRT(keys, minutes):

        html = "This plot shows the variation of peak width over the RT dimension. <br> The data for these plots was taken from " \
               "OpenSwathWorkflow output: <br><ul><li>"
        html+="</li><li>".join(k for k in list(keys))
        html = html + "</ul>Each boxplot corresponds to a {} minute time interval and shows mean peak wifth and variation." \
               "Peak Width is calculated from the leftWidth and rightWidth columns. Alternativley, full widh at half" \
               "maximum (fwhm) could also be used to represent this metric".format(minutes)
        return html


    return (img_to_html(fig), describePWoverRT(keys, min), 'PWoverRT')

