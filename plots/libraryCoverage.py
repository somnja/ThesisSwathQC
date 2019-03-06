'''
plot a venn diagram of coverage of he assay library, based on peptides
'''

import math
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib_venn import venn3
from scripts.stuff import checkFilyType, img_to_html


def describe():
    html = "Venn diagram of library coverage. This can only be plotted if the library assay list was provided in tsv format. " \
           "Libraries in pqp format are currently not supported. <br>" \
           "Library coverage will be plotted from tsv files, if they were provided, otherwise it can also be plotted from osw files. <br>" \
           "Coverage of the merged file from pyprophet is inlcuded and will be plotted from tsv first, if bothe were provided.<br>" \
           ""
    return html


def libCoverage(ax, library, file, key):
    """
    add venn diagram to represent library coverage and decoys on given axis,
    call this function from pltLibCoverage
    :param ax: axes to plot on
    :param library: dataframe of library from tsv
    :param file: dataframe of swath output, osw or tsv
    :param source: either tsv or osw, tet the right column names
    :param title: string, title of subplot
    :return: -
    """

    swathcol = 'MODIFIED_SEQUENCE'
    decoy = 'DECOY'

    # process dataframes into sets for venn diagram
    # for DIA: drop (UniMod:4) from peptide string
    dia_peptides = set(file[file[decoy] == 0].loc[:, swathcol].str.replace("\(UniMod:4\)", ""))
    lib_peptides = set(library[library['decoy'] == 0].loc[:, 'PeptideSequence'])
    decoys = set(file[file[decoy] == 1])


    #plot
    v = venn3([ lib_peptides, dia_peptides, decoys], set_labels=('Library', 'DIA', 'Decoys'), ax=ax)
    # library patch
    v.get_patch_by_id('100').set_alpha(0.8)
    v.get_patch_by_id('100').set_color('coral')

    # DIA patch
    v.get_patch_by_id('110').set_alpha(0.8)
    v.get_patch_by_id('110').set_color('#3A78A4')
    # decoy patch
    v.get_patch_by_id('001').set_alpha(0.8)
    v.get_patch_by_id('001').set_color('#81e448')

    # adjust subset label positions
    v.get_label_by_id("A").set_x(-0.4)

    b = v.get_label_by_id("B")
    x, y = b.get_position()
    b.set_position((x + 0.1, y + 0.2))

    d = v.get_label_by_id("C")
    x, y = d.get_position()
    d.set_position((x + 0.1, y))
    ax.set_title(key)

def plot(dfdict, lib, cols=3):
    """

    :param dfdict:
    :param lib: as dataframe
    :param cols:
    :return:
    """
    # N: total number of subplots, (length of dict + pptsv)
    # add pptsv to dict, in order to oterate over them all
    if not any(lib):
        return ('<p class="missing">no library file was provided</p>', describe(), 'libCov')
    else:
        lib
        if 'PeptideSequence' not in lib.columns:
            lib = lib.rename(columns={'UNMODIFIED_SEQUENCE': 'PeptideSequence', 'DECOY': 'decoy'})
        N = len(dfdict)
        rows = int(math.ceil(N / cols))

        gs = gridspec.GridSpec(rows, cols)
        fig = plt.figure(figsize=(20, 7*rows))

        keys = dfdict.keys()
        keyindex = zip(range(N), keys)
        for n, key in keyindex:
            filetype = checkFilyType(key)
            df = dfdict[key]
            if filetype == 'tsv':
                df = df.rename(columns={'decoy': 'DECOY', 'FullPeptideName': 'MODIFIED_SEQUENCE'})
            # set ax
            ax = fig.add_subplot(gs[n])
            # plot on ax
            libCoverage(ax, lib, df, key)
        fig.subplots_adjust(hspace=.2, wspace=.001)

        plt.suptitle('Library Coverage')

        return (img_to_html(fig), describe(), 'libcov')

