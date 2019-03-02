import math
import matplotlib.pyplot as plt
from scripts.toHtml import img_to_html
from matplotlib import gridspec

plt.rcParams.update({'font.size': 16})


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

