import matplotlib.pyplot as plt
from matplotlib import gridspec
from scripts.stuff import img_to_html



def dScorePlotOsw(df, key, gs_inner, fig):
    contexts = set(df.CONTEXT)
    for i, context in zip(range(len(contexts)), contexts):
        sub_df = df[df.CONTEXT == context]
        ax = plt.Subplot(fig, gs_inner[i])
        sub_df[sub_df.decoy == 0].d_score.plot.density(label='Targets', title=(context+key[-8:]), ax=ax)
        sub_df[sub_df.decoy == 1].d_score.plot.density(label='Decoys',  ax=ax)
        sub_df[sub_df.decoy == 0].d_score.plot.hist(color='blue', bins=40, alpha=0.5, label="Targets", ax=ax)
        sub_df[sub_df.decoy == 1].d_score.plot.hist(color='green', bins=40, alpha=0.5,   label='Decoys', ax=ax)
        ax.set_xlabel('d-score')
        fig.add_subplot(ax)

        # todo : plot either histogram or densit plot


def dScorePlotTsv(fig, df, key, gs_inner):

    ax1 = plt.Subplot(fig, gs_inner[0])
    #ax2 = plt.Subplot(fig, gs_inner[1])
    df[df.decoy == 0].d_score.plot.density(label='Targets', ax=ax1, title=key)
   # df[df.decoy == 1].d_score.plot.density(label='Decoys', ax=ax1)

    #df[df.decoy == 0].d_score.plot.hist(color='blue', bins=40, alpha=0.5, label="Targets", ax=ax2)
    #df[df.decoy == 1].d_score.plot.hist(color='green', bins=40, alpha=0.5,   label='Decoys', ax=ax2)





def plot(dfdict):
    keys = dfdict.keys()
    N = len(dfdict)
    keyindex = zip(range(N), keys)
    rows = N

    gs_outer = gridspec.GridSpec(rows, 1)
    fig = plt.figure(figsize=(20, 7 * rows))
    for n, key in keyindex:
        df = dfdict[key]
        if 'osw' in key:
            subcols=3
            gs_inner = gridspec.GridSpecFromSubplotSpec(1, subcols, subplot_spec=gs_outer[n], wspace=0.2, hspace=0.2)
            dScorePlotOsw(df, key, gs_inner, fig)
        if 'tsv' in key:
            ax = fig.add_subplot(gs_outer[n])
            df[df.decoy == 0].d_score.plot.density(label='Targets', ax=ax, title=key)
            df[df.decoy == 1].d_score.plot.density(label='Decoys', ax=ax)

    plt.suptitle('d-score histograms')


    html = "d-scores <br>" \
               "density plot or histogram?".format()

    #return (img_to_html(fig), html, 'dscoredensity')
    return ('no_fig', html, 'dscoredensity')


#Todo: _ plot mscores/Qvalues

def mScoreplotOws(df, key, gs_inner, fig):
    contexts = set(df.CONTEXT)
    for i, context in zip(range(len(contexts)), contexts):
        sub_df = df[df.CONTEXT == context]
        ax = plt.Subplot(fig, gs_inner[i])
        sub_df[sub_df.decoy == 0].d_score.plot.density(label='Targets', title=(context+key[-8:]), ax=ax)
        sub_df[sub_df.decoy == 1].d_score.plot.density(label='Decoys',  ax=ax)
        sub_df[sub_df.decoy == 0].d_score.plot.hist(color='blue', bins=40, alpha=0.5, label="Targets", ax=ax)
        sub_df[sub_df.decoy == 1].d_score.plot.hist(color='green', bins=40, alpha=0.5,   label='Decoys', ax=ax)
        ax.set_xlabel('d-score')
        fig.add_subplot(ax)


def mScoredPlotTsv(fig, df, key, gs_inner):

    ax1 = plt.Subplot(fig, gs_inner[0])
    ax2 = plt.Subplot(fig, gs_inner[1])
    df[df.decoy == 0].d_score.plot.density(label='Targets', ax=ax1, title=key)
    df[df.decoy == 1].d_score.plot.density(label='Decoys', ax=ax1)

    df[df.decoy == 0].d_score.plot.hist(color='blue', bins=40, alpha=0.5, label="Targets", ax=ax2)
    df[df.decoy == 1].d_score.plot.hist(color='green', bins=40, alpha=0.5,   label='Decoys', ax=ax2)



def plotQvalue(dfdict):
    keys = dfdict.keys()
    N = len(dfdict)
    keyindex = zip(range(N), keys)
    rows = N

    gs_outer = gridspec.GridSpec(rows, 1)
    fig = plt.figure(figsize=(20, 7 * rows))
    for n, key in keyindex:
        df = dfdict[key]
        contexts = set(df.CONTEXT)
        gs_inner = gridspec.GridSpecFromSubplotSpec(1, subplot_spec=gs_outer[n], wspace=0.2, hspace=0.2)
        dScorePlotOsw(df, key, gs_inner, fig)

    plt.suptitle('d-score plot')


    html = "d-scores <br>" \
               "density plot or histogram?".format()
    return (img_to_html(fig), html, 'dscore_density')
