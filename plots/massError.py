import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scripts.stuff import checkFilyType, img_to_html


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

    ax.hist(meanerrors, bins=bins, alpha=0.8)
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


def describe():

    html = "This histogram shows the distribution of mean mass errors of each feature. The mean is calculated from the mass errors of all ions in a feature." \
           "<br>Careful; can only be plotted from swath tsv files"
    return html


def plot(dfdict, cols=2):
    if not any(dfdict):
        return ('<p class="missing">can only be plotted from swath TSV files</p>', describe(), 'masserror')
    else:
        keys = dfdict.keys()
        N = len(dfdict)
        if N < cols:
            cols = N
        keyindex = zip(range(N), keys)
        rows = int(math.ceil(N / cols))

        gs = gridspec.GridSpec(rows, cols)
        fig = plt.figure(figsize=(20, 10 * rows))

        last = N - 1
        for n, key in keyindex:
            filetype=checkFilyType(key)
            if filetype == 'osw':
                continue
            if n == last:
                color = '#3A78A4'
            else:
                color = 'coral'
            ax = fig.add_subplot(gs[n])
            df = dfdict[key]
            # plot on ax
            massError(ax, df, key)
        plt.suptitle('mean Mass Error')

        return (img_to_html(fig), describe(), 'meanMassError')
# --------------------------------------
# two dimensional histogram

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
