import math
import matplotlib.pyplot as plt
from scripts.stuff import img_to_html, checkFilyType
from matplotlib import gridspec

plt.rcParams.update({'font.size': 16})

# Todo: only ploting from pp tsv export makes sense?

def describe():
    html = "Scatter plot of iRT against iRT difference, plotted from pyprophet output files" \
           "<br>"
    return html


def iRTcorrelation(ax, df, key, decoy='decoy', group='transition_group_id', x_irt='iRT', y_irt='delta_iRT'):
    # plot from tsv
    # plot from OSW feature
    # mean irt error
    if checkFilyType(key)=='osw':
        df['delta_iRT'] = df['iRT'] - df['LIBRARY_RT']
        df[df[decoy]==0].groupby('precursor').mean().plot.scatter(x='iRT', y='delta_iRT', ax=ax)

    else:
        df[df[decoy] == 0].groupby(group).mean().plot.scatter(x=x_irt, y=y_irt, ax=ax)
    plt.title(key)
    plt.xlabel('normalized RT [min]')


def plot(dfdict):
    if not any(dfdict):
        return "<p class='missing'>No pp tsv or osw file provided</p>"
    else:
        cols=1
        keys = dfdict.keys()
        N = len(dfdict)
        if N < cols:
            cols = N
        keyindex = zip(range(N), keys)
        rows = int(math.ceil(N / cols))

        gs = gridspec.GridSpec(rows, cols)
        fig = plt.figure(figsize=(20, 7 * rows))

        for n, key in keyindex:
            ax = fig.add_subplot(gs[n])
            df = dfdict[key]
            iRTcorrelation(ax, df, key)
            plt.subplots_adjust(hspace=.2, wspace=.001)
        fig.suptitle('RT correlation with library')

        return (img_to_html(fig), describe(), 'rtcorr')

