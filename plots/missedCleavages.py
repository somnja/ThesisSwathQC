'''
from: swath tsv only
'''
import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scripts.stuff import checkFilyType, img_to_html


def describe():
    html = "For each sequence, OpenSwathWorkflow does an in situ digest (assuming Trypsin) and places the number of missed " \
           "cleavages for each peptide in a column 'MC'. This columns can currently only be found in the tsv output from " \
           "OpenSwathWorkflow, so this plot will only be available if swath tsv file(s) were provided.<br>" \
           "Processing data: all peptides tagged as decoys are dropped before plotting and transitions groups are grouped" \
           "so that each peptide is counted only once.<br> QC target: sample preparation"
    return html


def missedCleavagesTsv(ax, df, key):
    temp_df = df[df.decoy == 0][['transition_group_id', 'MC']].drop_duplicates('transition_group_id').groupby(
        'MC').count()
    temp_df = temp_df.rename({'transition_group_id': 'peptides'}, axis=1)
    #sum = len(list(set(temp_df['peptides'])))
    #textstr = 'total number of peptides: {}'.format(sum)

    props = dict(boxstyle='round', facecolor='w', alpha=0.5)
    # place a text box in upper left in axes coords

    temp_df.plot(kind='bar', ax=ax, color="coral")
    ax.set_alpha(0.8)
    ax.set_title(key)  # , fontsize=14)
    ax.set_xlabel('# missed cleavages')
    ax.set_ylabel('count (transitions groups)')
    ax.legend('')
    ax.xaxis.set_tick_params(rotation=0)
    #ax.text(0.6, 0.9, textstr, transform=ax.transAxes,
     #       verticalalignment='top', bbox=props)


def plot(dfdict, cols=3):

    if not any(dfdict):
        return ('<p class="missing">can only be plotted from swath TSV </p>', describe(), 'masserror')
    else:
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
            missedCleavagesTsv(ax, df, key)
            plt.subplots_adjust(hspace=.2, wspace=.001)
        fig.suptitle('Missed Cleavages in peptides')


        return (img_to_html(fig), describe(), 'missedCleav')