import matplotlib.pyplot as plt
import math
from matplotlib import gridspec
from scripts.stuff import img_to_html



def densityPlot(ax, ax2, df, key):
    if key.lower().endswith('tsv'):
        df[df.decoy == 0].d_score.plot.density(label='Targets', ax=ax)
        df[df.decoy == 1].d_score.plot.density(label='Decoys', ax=ax)

        df[df.decoy == 0].d_score.plot.hist(color='blue', bins=40, alpha=0.5, label="Targets", ax=ax2)
        df[df.decoy == 1].d_score.plot.hist(color='green', alpha=0.5,   label='Decoys', ax=ax2)


def plot(dfdict, cols=2):
    keys = dfdict.keys()
    N = len(dfdict)
    if N < cols:
        cols = cols
    keyindex = zip(range(N), keys)
    rows = int(math.ceil(N / cols))

    gs = gridspec.GridSpec(rows, cols)
    fig = plt.figure(figsize=(20, 7 * rows))
    for n, key in keyindex:
        ax = fig.add_subplot(gs[n])
        ax2 =fig.add_subplot(gs[n+1])
        df = dfdict[key]
        # plot on ax
        densityPlot(ax, ax2, df, key)
    plt.suptitle('d-score density plot')

    def describe():
        html = "Density plot<br>" \
               ""
        return html
    return (img_to_html(fig), describe(), 'dscore_density')