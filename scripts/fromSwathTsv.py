''' from swath output file or files:
- masserror
'''
import numpy as np
import matplotlib.pyplot as plt
from  scripts.toHtml import img_to_html


def mNumOfTransitions(dfdict, b=3):

    # from dict of dataframes, determine number of columns and rows (default: 3 in a row)
    numdfs = len(dfdict)
    b = b
    if numdfs <= b:
        ncols = numdfs
        nrows = 1
    if numdfs > b:
        ncols = b
        nrows = int(numdfs/b) + 1

    fig, ax = plt.subplots(nrows, ncols, figsize=(20,7))

    for a, key in zip(ax, dfdict.keys()):
        print(a)
        df = dfdict[key]
        df_to_plot = df.groupby(["transition_group_id"]).count()["decoy"].value_counts().sort_index().to_frame().rename(columns = {'decoy':'number of peptides'})
        a.bar(df_to_plot.index, df_to_plot['number of peptides'])
        a.set_alpha(0.8)
        a.set_title(key, fontsize=14)
        a.set_ylabel("number of peptides", fontsize=14)
        a.set_xlabel("number of transitions", fontsize=14)
        a.xaxis.set_tick_params(rotation=0)
        # labels
        totals = []

        for i in a.patches:
            totals.append(i.get_height())

        total = sum(totals)
        a.legend("")

        for i in a.patches:
            a.text(i.get_x()-0.4, i.get_height()+30, str(i.get_height()), fontsize=12, color='dimgrey')
    return img_to_html(fig)


def meanError(entrystr):
    """for given strin, that conatins Apek m/z and masserror seperated by semicolon
    split string into list, take every second element (the masserror)
    ;return mean masserror """
    temp_list = entrystr.split(';')
    tmp_list = list(map(float, temp_list))
    return np.mean(list(tmp_list[i] for i in range(1, len(tmp_list), 2)))


def plotMassError(df):
    # masserror column into list of string
    masserrors = list(df.loc[:, 'masserror_ppm'].dropna())
    # lsit of mean mass errors
    meanerrors = [meanError(i) for i in masserrors]

    fig, ax = plt.subplots()
    bins = np.arange(min(meanerrors), max(meanerrors), 1)
    mu = np.mean(meanerrors)
    median = np.median(meanerrors)
    sigma = np.std(meanerrors)
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu,),
        r'$\mathrm{median}=%.2f$' % (median,),
        r'$\sigma=%.2f$' % (sigma,)))

    plt.hist(meanerrors, bins=bins, alpha=0.5)
    plt.title('Histogram of mean masserrors of transitions')
    plt.xlabel('masserror')
    plt.ylabel('count')
    # vertical line for mean
    # plt.axvline(mean,color='b', linewidth=1)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='w', alpha=0.5)
    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    return fig


def mPlotMassError(dfdict, b=3):
    numdfs = len(dfdict)
    if numdfs == 1:
        key = list(dfdict.keys())[0]
        df = dfdict[key]
        fig = plotMassError(df)

    else:
        b = b
        if numdfs <= b:
            ncols = numdfs
            nrows = 1
        if numdfs > b:
            ncols = b
            nrows = int(numdfs / b) + 1

        fig, ax = plt.subplots(nrows, ncols, figsize=(24, 14))

        for a, key in zip(ax, dfdict.keys()):
            df = dfdict[key]
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

            a.hist(meanerrors, bins=bins, alpha=0.8)
            a.set_title(key, fontsize=14)
            a.set_ylabel("count", fontsize=14)
            a.set_xlabel("mean masserror [ppm]", fontsize=14)
            # these are matplotlib.patch.Patch properties
            props = dict(boxstyle='round', facecolor='w', alpha=0.5)
            # place a text box in upper left in axes coords
            a.text(0.05, 0.95, textstr, transform=a.transAxes, fontsize=12,
                   verticalalignment='top', bbox=props)
    return img_to_html(fig)


def twoDimHist(df):
    fig, ax = plt.subplots(figsize=(12,7))
    df_to_plot = df[['masserror_ppm', 'm/z']].dropna()
    df_to_plot['meanerror'] = df_to_plot['masserror_ppm'].apply(lambda x: meanError(x))
    xdata = df_to_plot['m/z']
    ydata = df_to_plot['meanerror']
    bins = np.arange(min(xdata), max(xdata), 1)

    plt.hist2d(xdata, ydata, bins=[100, 100], alpha=0.5)
    plt.ylabel('mean masserror of transition')
    plt.ylabel('m/z')
    plt.title('2d histogram of masserrors')
    plt.colorbar()

    return fig


def mTwoDimHist(dfdict, b=3):
    numdfs = len(dfdict)

    if numdfs == 1:
        key=list(dfdict.keys())[0]
        df = dfdict[key]
        fig = twoDimHist(df)

    else:
        b = b
        if numdfs <= b:
            ncols = numdfs
            nrows = 1
        if numdfs > b:
            ncols = b
            nrows = int(numdfs / b) + 1

        fig, ax = plt.subplots(nrows, ncols, figsize=(12, 7))

        for a, key in zip(ax, dfdict.keys()):

            df = dfdict[key]
            df_to_plot = df[['masserror_ppm', 'm/z']].dropna()
            df_to_plot['meanerror'] = df_to_plot['masserror_ppm'].apply(lambda x: meanError(x))
            xdata = df_to_plot['m/z']
            ydata = df_to_plot['meanerror']
            bins = np.arange(min(xdata), max(xdata), 1)

            a.hist2d(xdata, ydata, bins=[100, 100], alpha=0.5)
            a.set_ylabel('mean masserror of transition')
            a.set_xlabel('m/z')
            a.set_title('2d histogram of masserrors')
            #a.colorbar()

    return img_to_html(fig)


def missedCleavages(dfdict, b=2):
    """ dict of swath tsv files, the columns with missed cleavages 'MC' is only available in qc json (MS1 level only)
    and in swath tsv, not osw, not after pyprophet
    """
    numdfs = len(dfdict)
    if numdfs <= b:
        ncols = numdfs
        nrows = 1
    if numdfs > b:
        ncols = b
        nrows = int(numdfs / b) + 1

    sbplt = (nrows * 100 + ncols * 10)
    # adjust figure size to number of plots
    fig = plt.figure(figsize=(24, 14 * nrows), facecolor='w', edgecolor='k')
    fig.subplots_adjust(hspace=.5, wspace=.001)
    keys = dfdict.keys()
    n = len(keys)
    keyindex = zip(range(1, len(keys) + 1), keys)

    for i, key in keyindex:
        df = dfdict[key]
        temp_df = df[df.decoy == 0][['transition_group_id', 'MC']].drop_duplicates('transition_group_id').groupby(
            'MC').count()
        temp_df = temp_df.rename({'transition_group_id': 'peptides'}, axis=1)
        sum = temp_df.sum()[0]
        ax = fig.add_subplot(sbplt + i)
        textstr =  'total number of peptides: {}'.format(sum)

        props = dict(boxstyle='round', facecolor='w', alpha=0.5)
        # place a text box in upper left in axes coords

        temp_df.plot(kind='bar', figsize=(12,7), ax=ax, color="coral", fontsize=14)
        ax.set_alpha(0.8)
        ax.set_title('Missed Cleavages '+key)#, fontsize=14)
        ax.set_xlabel('# missed cleavages', fontsize=13)
        ax.set_ylabel('count', fontsize=13)
        ax.xaxis.set_tick_params(rotation=0)
        ax.text(0.6, 0.9, textstr, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', bbox=props)
        plt.subplots_adjust(hspace=.5, wspace=.001)
    fig.suptitle('Missed Cleavages in peptides')

    return img_to_html(fig)






