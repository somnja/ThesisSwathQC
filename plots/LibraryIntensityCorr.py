import math
import numpy as np
import matplotlib.pyplot as plt
from scripts.stuff import img_to_html, checkFilyType
from matplotlib import gridspec

def describe():
    html = "The correlation of assay library (DDA) intensity with DIA intensity is calculated by OpenSwathWorkflow as one" \
           " of many sub-scores, that describe describe the peak group. This score is plotted here as boxplot for each provided swath output" \
           " file.<br>" \
           ""
    return html


def libraryCorr(ax, df, colname, key):
    """ boxplot of column 'var_library_corr' or 'VAR_LIBRARY_CORR (in all except pp exprot tsv)"""
    lib_corr = df[colname]
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



def plot(dfdict, cols=3):
    # osw: FEATURE_MS2
    if not any(dfdict):
        return ('<p class="missing">missing files </p>', describe(), 'libCorr')
    keys = dfdict.keys()


    N = len(dfdict)
    if N <= cols:
        cols = N

    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 7 * rows))

    for n, key in keyindex:
        if key.lower().endswith('tsv'):
            colname = 'var_library_corr'
        else:
            colname = 'VAR_LIBRARY_CORR'
        # set ax
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        libraryCorr(ax, df, colname, key)

    fig.subplots_adjust(hspace=.2, wspace=.001)
    fig.suptitle('Library Correlation')
    return (img_to_html(fig), describe(), 'libCorr')