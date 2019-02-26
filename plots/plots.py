import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from scripts.toHtml import img_to_html
from matplotlib import gridspec

plt.rcParams.update({'font.size': 16})

def IDoverRT(ax, df, title, RTcolumn, min):
    """ plot the number of Identifications for specified minute interval min , default: 5 min
    datasource: an:  pyprophet or swath, osw or tsv,
    :params df, raw dataframe from any file, RTcolumn: 'RT' for pptsv, or swath tsv, 'EXP_RT' fow pp osw and swath osw
    :return figure formatted as html string"""

    # bin RT range
    RTrange = np.arange(int(df.loc[:, RTcolumn].min()), int(df.loc[:, RTcolumn].max()), 60*min)
    # group by time interval and count
    # library patch
    ax.hist(df.loc[:, RTcolumn], bins=RTrange, color='coral', edgecolor="k")
    plt.title(title, fontsize=14)
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

def pltIDoverRT(dfdict, min=5, cols=2):
    """ plot nultiple subfugires
        plot the number of Identifications for specified minute interval min , default: 5 min
        datasource: this can be plotted from any file: pyprophet or swath, osw or tsv,
        :params df, raw dataframe from any file, RTcolumn: 'RT' for pptsv, or swath tsv, 'EXP_RT' fow pp osw and swath osw
        :return figure formatted as html string"""
    # N: total number of subplots, (length of dict + pptsv)
    # add pptsv to dict, in order to oterate over them all
    keys = dfdict.keys()
    if list(keys)[0].endswith('.osw'):
        RTcolumn = 'EXP_RT'
    if list(keys)[0].endswith('.tsv'):
        RTcolumn = 'RT'

    N = len(dfdict)
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(24, 7*rows))

    for n, key in keyindex:
        # set ax
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        IDoverRT(ax, df, key, RTcolumn, min)
    fig.subplots_adjust(hspace=.3, wspace=.001)

    plt.suptitle('ID over RT')
    return img_to_html(fig)


# --------------------
def PWoverRT(ax, df, title, source, min):
    """
    process dataframe and plot from axis, call this function from pltPWoverRT
    plot styling
    :param ax: axis to plot on
    :param df: datframe from dict
    :param title: set dataframe key as title
    :param source: osw or tsv
    :param min: time interval to bin boxed
    """
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
    xlabs = [5*i for i in range(len(RTrange))]
    df_to_plot = df.loc[:, [RWcolumn, LWcolumn, RTcolumn]]
    df_to_plot['widthDiff'] = df_to_plot.loc[:, RWcolumn] - df_to_plot.loc[:, LWcolumn]
    df_to_plot['bin'] = pd.cut(df_to_plot.loc[:, RTcolumn], RTrange)

    df_to_plot.boxplot(column='widthDiff', by='bin', rot=90, grid=False, figsize=(20, 7), ax=ax)
    ax.set_title(title)
    ax.set_xlabel('RT [in {} min intervals]'.format(str(min)))
    ax.set_ylabel('PeakWidth [ppm]')
    xtickNames = plt.setp(ax, xticklabels=xlabs)
    plt.setp(xtickNames, rotation=45, fontsize=14)


def pltPWoverRT(dfdict, min=5, cols=1):
    """
    boxplots of Peak Width for given dict of dataframesw, arrange plots deppending on size of dataframe
    determine osw or tsv source from dataframe keys
    :param dfdict: dict of dataframes, either from tsv or osw
    :param min: time interval on RT, default 5 min
    :param cols: number of subplots per column, default: 1
    :return: fig as html
    """

    keys = dfdict.keys()
    if list(keys)[0].endswith('.osw'):
        source = 'osw'
    if list(keys)[0].endswith('.tsv'):
        source = 'tsv'

    N = len(dfdict)
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 7 * rows))

    for n, key in keyindex:
        # set ax
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        PWoverRT(ax, df, key, source, min)

    fig.subplots_adjust(hspace=.4, wspace=.01)
    fig.suptitle('PeakWidth over RT')
    return img_to_html(fig)


# ------------------------------------------------------------

def libraryCorr(ax, df, colname, key):
    """ boxplot of column 'var_library_corr' or 'VAR_LIBRARY_CORR (in all except pp exprot tsv)"""

    lib_corr = df.loc[:, colname]
    # get mean, median and std error to place in textbox
    mu = np.mean(lib_corr)
    median = np.median(lib_corr)
    sigma = np.std(lib_corr)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu,),
        r'$\mathrm{median}=%.2f$' % (median,),
        r'$\sigma=%.2f$' % (sigma,)))
    ax.boxplot(lib_corr)
    #plt.title('Intensity Correlation with Library')
    ax.set_xlabel(key)
    ax.set_ylabel(colname)
    # vertical line for mean
    # plt.axvline(mean,color='b', linewidth=1)

    # these are matplotlib.patch.Patch properties
    props = dict(facecolor='w', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)



def pltLibCorr(dfdict, cols=3):
    keys = dfdict.keys()
    if list(keys)[0].endswith('.osw'):
        colname = 'VAR_LIBRARY_CORR'
    if list(keys)[0].endswith('.tsv'):
        colname = 'var_library_corr'

    N = len(dfdict)
    if N <= cols:
        cols = N

    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 7 * rows))

    for n, key in keyindex:
        # set ax
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        libraryCorr(ax, df, colname, key)

    fig.subplots_adjust(hspace=.2, wspace=.001)
    fig.suptitle('Library Correlation')
    return img_to_html(fig)

# -------------------------------------------------------------------
def libCoverage(ax, library, file, source, title='library Coverage'):
    """
    add venn diagram to represent library coverage and decoys on given axis,
    call this function from pltLibCoverage
    :param ax: axes to plot on
    :param library: dataframe of library from tsv
    :param file: dataframe of swath output, osw or tsv
    :param source: either tsv or osw, tet the right column names
    :param title: string, title of subplot
    :return: -
    """
    # set column names depending on file type
    if source == 'osw':
        swathcol = 'MODIFIED_SEQUENCE'
        decoy = 'DECOY'
    if source == 'tsv':
        swathcol = 'FullPeptideName'
        decoy = 'decoy'
    # process dataframes into sets for venn diagram
    # for DIA: drop (UniMod:4) from peptide string
    dia_peptides = set(file[file[decoy] == 0].loc[:, swathcol].str.replace("\(UniMod:4\)", ""))
    lib_peptides = set(library[library['decoy'] == 0].loc[:, 'PeptideSequence'])
    decoys = set(file[file[decoy] == 1])


    #plot
    v = venn3([ lib_peptides, dia_peptides, decoys], set_labels=('Library', 'DIA', 'Decoys'), ax=ax)
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
    if 'PeptideSequence' not in lib.columns:
        lib = lib.rename(columns={'UNMODIFIED_SEQUENCE': 'PeptideSequence', 'DECOY': 'decoy'})
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


# --------------------------------------------
# from TSv only
def numOfTransitions(ax, df, key):
    """number of transitions for each identified peptide
    datasource: pptsv
    :param pptsv dataframe
    :return figure as html
    """

    df_to_plot = df.groupby(["transition_group_id"]).count()["decoy"].value_counts().sort_index().to_frame().rename(
        columns={'decoy': 'number of peptides'})
    ax.bar(df_to_plot.index, df_to_plot['number of peptides'], color='coral')
    bins = np.arange(1, df_to_plot.index.max() +1)

    #ax.hist(df_to_plot.iloc[:, 0], bins=bins, color='coral', edgecolor="k")
    plt.xticks(bins)
    ax.set_alpha(0.8)
    ax.set_title(key, fontsize=14)
    ax.set_ylabel("number of peptides")
    ax.set_xlabel("number of transitions")
    # labels
    totals = []
    for i in ax.patches:
        totals.append(i.get_height())
    #ax.legend("")
    for i in ax.patches:
        ax.text(i.get_x(), i.get_height() + 40, str(i.get_height()))



def pltNumOfTransitions(dfdict, cols=2):
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 10 * rows))

    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        # plot on ax
        numOfTransitions(ax, df, key)
    plt.suptitle('')
    return img_to_html(fig)

###---------------------
### from TSV only !!
###---------------------


def meanError(entrystr):
    """for given strin, that conatins Apek m/z and masserror seperated by semicolon
    split string into list, take every second element (the masserror)
    ;return mean masserror """
    temp_list = entrystr.split(';')
    tmp_list = list(map(float, temp_list))
    return np.mean(list(tmp_list[i] for i in range(1, len(tmp_list), 2)))


def massError(ax, df, key):
    # masserror column into list of string
    masserrors = list(df.loc[:, 'masserror_ppm'].dropna())
    # lsit of mean mass errors
    meanerrors = [meanError(i) for i in masserrors]


    bins = np.arange(min(meanerrors), max(meanerrors), 1)
    mu = np.mean(meanerrors)
    median = np.median(meanerrors)
    sigma = np.std(meanerrors)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu,),
        r'$\mathrm{median}=%.2f$' % (median,),
        r'$\sigma=%.2f$' % (sigma,)))

    ax.hist(meanerrors, bins=bins, alpha=0.5)
    plt.title(key)
    plt.xlabel('masserror')
    plt.ylabel('count')
    # vertical line for mean
    # plt.axvline(mean,color='b', linewidth=1)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='w', alpha=0.5)
    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)

def pltMassError(dfdict, cols=2):

    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 10 * rows))

    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        # plot on ax
        massError(ax, df, key)
    plt.suptitle('mean Mass Error')

    return img_to_html(fig)
# --------------------------------------


def twoDimHist(ax, df, key):

    df_to_plot = df[['masserror_ppm', 'm/z']].dropna()
    df_to_plot['meanerror'] = df_to_plot['masserror_ppm'].apply(lambda x: meanError(x))
    xdata = df_to_plot['m/z']
    ydata = df_to_plot['meanerror']
    bins = np.arange(min(xdata), max(xdata), 1)

    ax.hist2d(xdata, ydata, bins=[100, 100], alpha=0.5)
    plt.ylabel('mean masserror of transition')
    plt.ylabel('m/z')
    plt.title(key)


def pltTwoDimHist(dfdict, cols=3):
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 10 * rows))

    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        twoDimHist(ax, df, key)
    plt.suptitle('2D Histogram masserrors')
    #plt.colorbar()

    return img_to_html(fig)


def missedCleavages(ax, df, key):
    temp_df = df[df.decoy == 0][['transition_group_id', 'MC']].drop_duplicates('transition_group_id').groupby(
        'MC').count()
    temp_df = temp_df.rename({'transition_group_id': 'peptides'}, axis=1)
    #sum = len(list(set(temp_df['peptides'])))
    #textstr = 'total number of peptides: {}'.format(sum)

    props = dict(boxstyle='round', facecolor='w', alpha=0.5)
    # place a text box in upper left in axes coords

    temp_df.plot(kind='bar', ax=ax, color="coral")
    ax.set_alpha(0.8)
    ax.set_title('Missed Cleavages ' + key)  # , fontsize=14)
    ax.set_xlabel('# missed cleavages')
    ax.set_ylabel('count')
    ax.legend('')
    ax.xaxis.set_tick_params(rotation=0)
    #ax.text(0.6, 0.9, textstr, transform=ax.transAxes,
     #       verticalalignment='top', bbox=props)

def pltMissedCleavages(dfdict, cols=2):
    """ dict of swath tsv files, the columns with missed cleavages 'MC' is only available in qc json (MS1 level only)
    and in swath tsv, not osw, not after pyprophet
    """
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 10 * rows))

    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        missedCleavages(ax, df, key)
        plt.subplots_adjust(hspace=.2, wspace=.001)
    fig.suptitle('Missed Cleavages in peptides')

    return img_to_html(fig)

def iRTcorrelation(ax, df, key, decoy='decoy', group='transition_group_id', x_irt='iRT', y_irt='delta_iRT'):
    # plot from tsv
    # plot from OSW
    # mean irt error
    if 'transition_group_id' not in df.columns:
        df.plot.scatter(x='NORM_RT', y='DELTA_RT', ax=ax)
    else:
        df[df[decoy] == 0].groupby(group).mean().plot.scatter(x=x_irt, y=y_irt, ax=ax)
    plt.title(key)

def pltIRTCorr(dfdict, cols=2):
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 10 * rows))

    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        iRTcorrelation(ax, df, key)
        plt.subplots_adjust(hspace=.2, wspace=.001)
    fig.suptitle('iRT correlation')

    return img_to_html(fig)


def multiplot(dfdict, plotfunction, cols=2):
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 10 * rows))

    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        plotfunction
        plt.subplots_adjust(hspace=.2, wspace=.001)
    fig.suptitle('Missed Cleavages in peptides')

    return img_to_html(fig)