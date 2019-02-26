''' format the descrption texts for each plot type
they also should include som printed out informatio about the used dataframe etc'''


def describeIDoverRT(filetype, minutes=5):
    """return html string , filetype is either 'tsv' or 'osw'"""
    html = "This histogram shows the number of Identifications made in each retention time interval. In this plot, each " \
           "bar represents a {} minute interval, the actual retention time is displayed in seconds on the x axis.<br>" \
           "These plots can be generated from OpenSwathWorkflow output files, that can be either in either in tsv or osw fromat. " \
           "In this case, {} files were used. For each given input file a subplot is generated<br> Please compare runs and make sure, " \
           "the number of IDs are stable over RT dimension and between runs".format(minutes, filetype)
    return html

def describePWoverRT(filetype, minutes=5):
    html = "This plot shows the variation of peak width over the RT dimension. <br> The data for these plots was taken from " \
           "OpenSwathWorkflow output in {} format. Peak Width is calculated from the leftWidth and rightWidth columns." \
           " RT was grouped into {} minute time interval and a boxplot for each time interval show the mean peak width and " \
           "the variation of the data".format(filetype, minutes)

    return html

def describeMissedCleavages():
    html = "For each sequence, OpenSwathWorkflow does an in situ digest (assuming Trypsin) and places the number of missed " \
           "cleavages for each peptide in a column 'MC'. This columns can currently only be found in the tsv output from " \
           "OpenSwathWorkflow, so this plot will only be available if swath tsv file(s) were provided.<br>" \
           "Processing data: all peptides tagged as decoys are dropped before plotting and transitions groups are grouped" \
           "so that each peptide is counted only once.<br> QC target: sample preparation"
    return html

def describeNofTransitions():
    html = "Each Transitions group (peptide) might get identified multiple times during a run. This histogram shows the distribution, of how often peptides were identified. <br>" \
           "This plot is only available from tsv"
    return html



def describeMasserror():
    return 0


def describeLibraryCorr(filetype):
    html = "The correlation of assay library (DDA) intensity with DIA intensity is calculated by OpenSwathWorkflow as one" \
           " of many sub-scores, that describe describe the peak group. This score is plotted here as boxplot for each provided swath {}" \
           " file.".format(filetype)
    return html


def describeLibCoverage(source):
    html = "Venn diagram of library coverage. This can only be plotted if the library assay list was provided in tsv format. " \
           "Libraries in pqp format are currently not supported. <br>" \
           "Library coverage wil be plotted from tsv files, if they were provided, otherwise it can also be plotted from osw files. <br>" \
           "Coverage of the merged file from pyprophet is inlcuded and will be plotted from tsv first, if bothe were provided.<br>" \
           "".format(source)
    return html



