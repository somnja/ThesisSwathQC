import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import numpy as np
from scripts.toHtml import img_to_html
from plots.barplot import barplot
from matplotlib import gridspec
import math

plt.rcParams.update({'font.size': 16})
def IDoverRT(df, RTcolumn, min=5,  figsize=(12, 7)):
    """ plot the number of Identifications for specified minute interval min , default: 5 min
    datasource: this can be plotted from any file: pyprophet or swath, osw or tsv,
    :params df, raw dataframe from any file, RTcolumn: 'RT' for pptsv, or swath tsv, 'EXP_RT' fow pp osw and swath osw
    :return figure formatted as html string"""

    # bin RT range
    RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), 60*min)
    # group by time interval and count
    # df_to_plot= pptsv.groupby(pd.cut(pptsv[RTcolumn], RTrange))['filename'].count()
    fig, ax = plt.subplots(figsize=figsize)
    plt.hist(df.RT, bins=RTrange, color='coral', edgecolor="k")
    plt.title('IDs over RT', fontsize=14)
    plt.xlabel('RT[sec]', fontsize=13)
    plt.ylabel('# of IDs', fontsize=13)
    plt.xticks(RTrange)
    # style x and y labels:
    for label in ax.yaxis.get_ticklabels():
        label.set_fontsize(12)
    for label in ax.xaxis.get_ticklabels():
        # label is a Text instance
        # label.set_color('red')
        label.set_rotation(45)
        label.set_fontsize(12)
    return img_to_html(fig)


def mIDoverRT(dfdict, RTcolumn, min=5, b=2):
    """ plot nultiple subfugires
    plot the number of Identifications for specified minute interval min , default: 5 min
    datasource: this can be plotted from any file: pyprophet or swath, osw or tsv,
    :params df, raw dataframe from any file, RTcolumn: 'RT' for pptsv, or swath tsv, 'EXP_RT' fow pp osw and swath osw
    :return figure formatted as html string"""
    numdfs = len(dfdict)
    b = b
    if numdfs <= b:
        ncols = numdfs
        nrows = 1
    if numdfs > b:
        ncols = b
        nrows = int(numdfs / b) + 1

    keys = dfdict.keys()
    fig = plt.figure(figsize=(20,7))
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    for i, key in zip(range(1, len(keys)+1), keys):

        df = dfdict[key]
        RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), 60 * min)
        plt.subplot(nrows, ncols, i)
        plt.hist(df.loc[:, RTcolumn], bins=RTrange, color='coral', edgecolor="k")
        plt.title(('IDs over RT, '+key), fontsize=14)
        plt.xlabel('RT[sec]', fontsize=13)
        plt.ylabel('# of IDs', fontsize=13)
        plt.xticks(RTrange)
        # style x and y labels:

    return img_to_html(fig)
    # bin RT range


def PWoverRT(df, source, min=5):
    """Peak Width over RT,
    datasource: from any, plot from either any input file, swath or pyprophet osw(FEATURE) or tsv
    binning by 5 min interval (default)
    :param df from any source, tsv or osw, pp or swath; source: string of either 'tsv' or 'osw'
    :return image as html string"""
    # set column names based on df origin
    if source == 'tsv':
        RTcolumn='RT'
        RWcolumn = 'rightWidth'
        LWcolumn = 'leftWidth'
    if source == 'osw':
        RTcolumn = 'EXP_RT'
        RWcolumn = 'RIGHT_WIDTH'
        LWcolumn = 'LEFT_WIDTH'

    RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), 60 * min)
    df_to_plot = df.loc[:, [RWcolumn, LWcolumn, RTcolumn]]
    df_to_plot['widthDiff'] = df_to_plot.loc[:, RWcolumn] - df_to_plot.loc[:, LWcolumn]
    df_to_plot['bin'] = pd.cut(df_to_plot.loc[:, RTcolumn], RTrange)

    ax = df_to_plot.boxplot(column='widthDiff', by='bin', rot=90, grid=False, figsize=(20, 7))
    fig = ax.get_figure()
    return img_to_html(fig)


def mPWoverRT(dfdict, source, min=5, b=1):
    if source == 'tsv':
        RTcolumn = 'RT'
        RWcolumn = 'rightWidth'
        LWcolumn = 'leftWidth'
    if source == 'osw':
        RTcolumn = 'EXP_RT'
        RWcolumn = 'RIGHT_WIDTH'
        LWcolumn = 'LEFT_WIDTH'
    numdfs = len(dfdict)
    ncols = b
    nrows = numdfs

    sbplt = (nrows * 100 + ncols * 10)
    # adjust figure size to number of plots
    fig = plt.figure(figsize=(20, 7*nrows), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.5, wspace=.001)
    keys = dfdict.keys()
    n = len(keys)

    keyindex = zip(range(1, len(keys) + 1), keys)

    for i, key in keyindex:
        ax = fig.add_subplot(sbplt + i)
        df = dfdict[key]
        RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), 60 * min)
        df_to_plot = df.loc[:, [RWcolumn, LWcolumn, RTcolumn]]
        df_to_plot['widthDiff'] = df_to_plot.loc[:, RWcolumn] - df_to_plot.loc[:, LWcolumn]
        df_to_plot['bin'] = pd.cut(df_to_plot.loc[:, RTcolumn], RTrange)
        df_to_plot.boxplot(column='widthDiff', by='bin', ax=ax, rot=90, grid=False, figsize=(20, 7))
        ax.set_title(str(sbplt + i) + ' ' + key)
        plt.subplots_adjust(hspace=.5, wspace=.001)
    fig.suptitle('title')
    return img_to_html(fig)


def numOfTransitions(df):
    """number of transitions for each identified peptide
    datasource: pptsv
    :param pptsv dataframe
    :return figure as html
    """
    df_to_plot = df.groupby(["transition_group_id"]).count()["decoy"].value_counts().sort_index().to_frame().rename(
        columns={'decoy': 'number of peptides'})
    fig = barplot(df_to_plot, "Number of Transitions", "# peptides", "# transitions")
    return img_to_html(fig)


def libraryCorr(dfdict, source, b=3):
    """ boxplot of column 'var_library_corr' or 'VAR_LIBRARY_CORR (in all except pp exprot tsv)"""
    if source == 'tsv':
        colname = 'var_library_corr'
    if source == 'osw':
        colname = 'VAR_LIBRARY_CORR'
    numdfs = len(dfdict)
    if numdfs <= b:
        ncols = numdfs
        nrows = 1
    if numdfs > b:
        ncols = b
        nrows = int(numdfs / b) + 1
    # plot basename: (21i)
    sbplt = (nrows * 100 + ncols * 10)
    # adjust figure size to number of plots
    fig = plt.figure(figsize=(20, 7*nrows), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.5, wspace=.001)
    keys = dfdict.keys()

    keyindex = zip(range(1, len(keys) + 1), keys)

    for i, key in keyindex:
        ax = fig.add_subplot(sbplt + i)
        df = dfdict[key]
        # place mean median and std in textbox
        lib_corr = df.loc[:, colname]
        mu = np.mean(lib_corr)
        median = np.median(lib_corr)
        sigma = np.std(lib_corr)
        textstr = '\n'.join((
            r'$\mu=%.2f$' % (mu,),
            r'$\mathrm{median}=%.2f$' % (median,),
            r'$\sigma=%.2f$' % (sigma,)))
        plt.boxplot(lib_corr)
        #plt.title('Intensity Correlation with Library')
        plt.xlabel(key)
        plt.ylabel(colname)
        # vertical line for mean
        # plt.axvline(mean,color='b', linewidth=1)

        # these are matplotlib.patch.Patch properties
        props = dict(facecolor='w', alpha=0.5)

        # place a text box in upper left in axes coords
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)

        #plt.subplots_adjust(hspace=.5, wspace=.001)
    fig.suptitle('Intensity Correlation with Library')
    return img_to_html(fig)


def libCoverage(ax, library, file, source, title='library Coverage'):
    # set of peptides on each file, for DIA: drop (UniMod:4) from peptide string
    if source == 'osw':
        swathcol = 'MODIFIED_SEQUENCE'
        decoy = 'DECOY'
    if source == 'tsv':
        swathcol = 'FullPeptideName'
        decoy = 'decoy'

    dia_peptides = set(file[file[decoy] == 0].loc[:, swathcol].str.replace("\(UniMod:4\)", ""))
    lib_peptides = set(library['PeptideSequence'])
    decoys = set(file[file[decoy] == 1])

    v = venn3([lib_peptides, dia_peptides, decoys], set_labels=('Library', 'DIA', 'Decoys'), ax=ax)
    # library patch
    v.get_patch_by_id('100').set_alpha(0.8)
    v.get_patch_by_id('100').set_color('coral')
    # DIA patch
    v.get_patch_by_id('110').set_alpha(0.8)
    v.get_patch_by_id('110').set_color('#3A78A4')
    # decoy patch
    v.get_patch_by_id('001').set_alpha(0.8)
    v.get_patch_by_id('001').set_color('#81e448')
    # adjust subset label positions
    v.get_label_by_id("A").set_x(-0.4)
    b = v.get_label_by_id("B")
    x, y = b.get_position()
    b.set_position((x + 0.1, y + 0.2))
    d = v.get_label_by_id("C")
    x, y = d.get_position()
    d.set_position((x + 0.1, y))
    ax.set_title(title)

def pltLibCoverage(swathdict, lib, pptsv, source='tsv', cols=3):
    """create one figure with subplots for all input dataframes"""
    # N: total number of subplots, (length of dict + pptsv)
    # add pptsv to dict, in order to oterate over them all
    if source == 'osw':
        pptsv = pptsv.rename(columns={'decoy': 'DECOY', 'FullPeptideName': 'MODIFIED_SEQUENCE'})

    swathdict['pp_merged'] = pptsv
    N = len(swathdict)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 7*rows))

    keys = swathdict.keys()
    keyindex = zip(range(N), keys)

    for n, key in keyindex:
        # set ax
        ax = fig.add_subplot(gs[n])
        # plot on ax
        libCoverage(ax, lib, swathdict[key], source, key)
    fig.subplots_adjust(hspace=.2, wspace=.001)

    plt.suptitle('Library Coverage')

    return img_to_html(fig)


