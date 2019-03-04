import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
from scripts.stuff import checkFilyType, img_to_html, colorPP


def numPeaks(entrystr):
    temp_list = [i for i in entrystr.split(';') if float(i) != 0]
    return len(temp_list)

def numOfTransitions(ax, df, key, color):
    """number of transitions for each identified peptide
    datasource: pptsv, swathtsv, stwathosw:feature_transition table
    :param pptsv dataframe
    :return figure as html
    """
    # from tsv:
    if checkFilyType(key) == 'tsv':
        df['peak_count'] = df['aggr_Peak_Area'].apply(lambda x: numPeaks(x))
        to_plot = df[df['decoy'] == 0].groupby('peak_count').count().reset_index().rename(columns={'transition_group_id':'number of available peaks'})
        to_plot.plot.bar(x='peak_count', y='number of available peaks', color=color, edgecolor='k', ax=ax, legend=None)
    if checkFilyType(key) == 'osw':
        # from FEATURE_TRANSITION table
        # either APEX_INTENSITY or AREA_INTENSITY
        to_plot = df[df.APEX_INTENSITY != 0.0].groupby('FEATURE_ID').count().groupby('TRANSITION_ID').count().reset_index().rename(
            columns={'TRANSITION_ID': 'peak_count', 'AREA_INTENSITY': 'number of available peaks'})
        to_plot.plot.bar(x='peak_count',  y='number of available peaks', color=color, edgecolor='k', ax=ax, sharey=True, legend=None)

    ax.set_title(key)
    ax.set_ylabel("number of peptides")
    ax.set_xlabel("number of transitions")
    # labels
    totals = []
    for i in ax.patches:
        totals.append(i.get_height())
    #ax.legend("")
    for i in ax.patches:
        ax.text(i.get_x(), i.get_height() + 40, str(i.get_height()))



def plot(dfdict, filedict, cols=3):
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = N
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))
    # Todo: arrange plots, share y axis
    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 7 * rows))
    last = N - 1
    for n, key in keyindex:

        color= colorPP(key, filedict)
        ax = fig.add_subplot(gs[n])
        df = dfdict[key]
        # plot on ax
        numOfTransitions(ax, df, key, color)
    plt.suptitle('Number of Transitiion per feature')

    def describe():
        html = "Each feature has multiple transtions. to be precise, each has a count of 6, but since some the peaks" \
               " are empty and will therefore not be counted. " \
               "For tsv files, the number of available peaks can be counted from the column 'aggr_peak_area' is inspected. " \
               "It contains a list of peaks and their respective masserrors. For osw files, number of transitions can be " \
               "read from the table FEATURE_TRANSITION. it contains 6 transitions for each feature, but for some transitions, " \
               "no peak was actually detected. So only each non zero AREA_INTENSITY (or alternatively APEX_INTENSITY) will be counted." \
               " The file from pyprophet contains all features and transitions from merged swath files, s o the total number " \
               "will be much higher. But the number of features with only 1 - 3 transitions should go down considerably "
        return html
    return (img_to_html(fig), describe(), 'noOfTransitions')


