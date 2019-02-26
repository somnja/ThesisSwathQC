'''
for the sections:
- ID over RT
- Peak Width over RT
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scripts.toHtml import img_to_html
from plots.barplot import barplot


pptsv = pd.read_csv(r"C:\Users\Admin\PycharmProjects\MasterThesis\sample_input\merged_export.tsv", sep='\t')


def IDoverRT(pptsv, min=5, RTcolumn='RT', figsize=(12,7)):
    """plot th number of Identifications for specified minute interval min , default: 5min
    datasource: pyprophet tsv file (dataframe pptsv)
    :return image as html srting"""

    # bin RT range
    RTrange = np.arange(int(pptsv.RT.min()), int(pptsv.RT.max()), 60*min)  # maby roud to int or no
    # group by time interval and count
    # df_to_plot= pptsv.groupby(pd.cut(pptsv[RTcolumn], RTrange))['filename'].count()
    fig, ax = plt.subplots(figsize=figsize)
    plt.hist(pptsv.RT, bins=RTrange, color='coral', edgecolor="k")
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


def PWoverRT(df, min=5):
    """Peak Wiith over RT,
    plot from either pyprophet osw(FEATURE) or tsv, specify dataframe origin
    :return image as html string"""

    # check datafrme columsn names, they differ for osw and tsv
    # is tsv?
    if 'RT' in df.columns:
        RTrange = np.arange(int(df.RT.min()), int(df.RT.max()), 60 * min)
        df_to_plot = df.loc[:, ['rightWidth', 'leftWidth', 'RT']]
        df_to_plot['widthDiff'] = df_to_plot.loc[:,'rightWidth'] - df_to_plot.loc[:,'leftWidth']
        df_to_plot['bin'] = pd.cut(df_to_plot.RT, RTrange)

    if 'EXP_RT' in df.columns:
        RTrange = np.arange(int(df.EXP_RT.min()), int(df.EXP_RT.max()), 60 * min)
        df_to_plot = df[['RIGHT_WIDTH', 'LEFT_WIDTH', 'EXP_RT']]
        df_to_plot['widthDiff'] = df_to_plot.loc[:,'RIGHT_WIDTH'] - df_to_plot.loc[:,'LEFT_WIDTH']
        df_to_plot['bin'] = pd.cut(df_to_plot.EXP_RT, RTrange)

    ax = df_to_plot.boxplot(column='widthDiff', by='bin', rot=90, grid=False, figsize=(20, 10))
    fig = ax.get_figure()
    return img_to_html(fig)


def numOfTransitions(df):
    """number of transitions for each identified peptide
    :param pptsv dataframe
    :return figure as html
    """
    df_to_plot = df.groupby(["transition_group_id"]).count()["decoy"].value_counts().sort_index().to_frame().rename(
        columns={'decoy': 'number of peptides'})
    fig = barplot(df_to_plot, "Number of Transitions", "# peptides", "# transitions")
    return img_to_html(fig)


