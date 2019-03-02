import math
import numpy as np
import matplotlib.pyplot as plt
from scripts.toHtml import img_to_html
from matplotlib import gridspec
from scripts.stuff import checkFilyType


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
    last = N - 1
    for n, key in keyindex:

        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        # plot on ax
        numOfTransitions(ax, df, key)
    plt.suptitle('')

    def describe():
        html = "Each Transitions group (peptide) might get identified multiple times during a run. This histogram shows the distribution, of how often peptides were identified. <br>" \
               "This plot is only available from tsv"
        return html
    return (img_to_html(fig), describe(), 'noOfTransitions')


def describeNofTransitions():
    html = "Each Transitions group (peptide) might get identified multiple times during a run. This histogram shows the distribution, of how often peptides were identified. <br>" \
           "This plot is only available from tsv"
    return html
