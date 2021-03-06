from __future__ import print_function
import argparse
import os
import base64
from io import BytesIO
from scripts.handleOSW import *
from plots import PeakWidthOverRT, IDoverRT, numOfTransitions, massError, libraryCoverage, missedCleavages, \
    RtcorrWithLibrary, pyprophet_scores, LibraryIntensityCorr, featuresPerPeptide
from scripts.fileContentInfoTable import *



def img_to_html(figure):
    """
    convert hml figure into html string to avoid saving the image
    :param figure: plot figure object
    :return: hml formatted figure
    """
    buffer = BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)

    data_uri = base64.b64encode(buffer.read()).decode('ascii')
    html = '<img class="myImages" src="data:image/png;base64,{0}" >'.format(data_uri)
    return html


def renderImgSection(figureAndDescription, header, templateFolder='templates/', templateFile='sectionImg.html'):

    figurehtml = figureAndDescription[0]
    description = figureAndDescription[1]
    sectionid = figureAndDescription[2]
    env = Environment(loader=FileSystemLoader(templateFolder))  #path to templates; eg 'templates2/'
    template = env.get_template(templateFile) #"sample_prep.html"
    template_vars = {'id': sectionid,
                     'h': header,
                     'description': description,
                     'figure': figurehtml}
    html_out = template.render(template_vars)
    return html_out


def plotsFromDfdict(dfdict, filedict):

    #Todo: give pp different color in plots, (use filedict to compare key)
    sectionlist = []

    # prepare specific dicts to be passed to plotting functions
    overRT_dict = {}
    numOfTransitions_dict = {}
    masserror_dict = {}
    libCov_dict = {}
    missedCleav_dict = {}
    irt_dict = {}
    pp_score = {}
    libIntensity_dict = {}

    keys = dfdict.keys()
    if 'swath files' in filedict.keys() and filedict['swath files'][0].lower().endswith('tsv'):
        swath_dict = {k: dfdict[k] for k in filedict['swath files']}
        overRT_dict.update(swath_dict)
        numOfTransitions_dict.update(swath_dict)
        masserror_dict.update(swath_dict)
        libCov_dict.update(swath_dict)
        missedCleav_dict.update(swath_dict)
        libIntensity_dict.update(swath_dict)
    if 'swath files' in filedict.keys() and filedict['swath files'][0].lower().endswith('osw'):
        # unpack dict of dicts
        keyindex = zip(range(len(filedict['swath files'])), keys)
        swath_feature = {}
        swath_featureMS2 = {}
        swath_featureTransition = {}
        swath_peptide = {}
        for n, key in keyindex:
            dfs = dfdict[key]
            swath_feature[key] = dfs['feature']
            swath_featureMS2[key] = dfs['featureMS2']
            swath_featureTransition[key] = dfs['featureTransition']
            swath_peptide[key] = dfs['peptide']
        overRT_dict.update(swath_feature)
        numOfTransitions_dict.update(swath_featureTransition)
        libCov_dict.update(swath_peptide)
        libIntensity_dict.update(swath_featureMS2)

    # pp files :
    keylist = filedict['pyprophet']
    for key in keylist:
        if key.lower().endswith('tsv'):
            pp_dict = {key: dfdict[key]}
            overRT_dict.update(pp_dict)
            numOfTransitions_dict.update(pp_dict)
            libCov_dict.update(pp_dict)
            irt_dict.update(pp_dict)
            #pp_score.update(pp_dict)
        if key.lower().endswith('osw'):
            dfs = dfdict[key]
            pp_feature = {key: dfs['feature']}
            pp_peptide = {key: dfs['peptide']}
            pp_irt = {key: dfs['irt']}
            pp_featureMS2 = {key: dfs['featureMS2']}
            pp_peptidescore = {(key+'_peptide'): dfs['peptideScores']}
            pp_proteinscore = {(key+'_protein'): dfs['proteinScores']}
            pp_featureTransition = {key: dfs['featureTransition']}
            overRT_dict.update(pp_feature)
            numOfTransitions_dict.update(pp_featureTransition)
            libCov_dict.update(pp_peptide)
            irt_dict.update(pp_irt)
            libIntensity_dict.update(pp_featureMS2)
            pp_score.update(pp_peptidescore)
            pp_score.update(pp_proteinscore)

    # only plot library coverage if library is available
    if 'library' not in filedict.keys():
        lib = {}
        libCov_dict.update(lib)
        #Todo: library in tsv format!
    if 'library' in filedict.keys():
        key = filedict['library']
        dfs = dfdict[key]
        lib_transition = {key: dfs['transition']}
        lib_peptide = dfs['peptide']
        lib_protein = {key: dfs['protein']}

    print(libIntensity_dict.keys())
    sectionlist.extend([renderImgSection(PeakWidthOverRT.plot(overRT_dict, filedict), 'PeakWidth over RT'),
                        renderImgSection(IDoverRT.plot(overRT_dict, filedict), 'ID over RT'),
                        renderImgSection(numOfTransitions.plot(numOfTransitions_dict, filedict), 'Number of Transitions'),
                        renderImgSection(massError.plot(masserror_dict), "Mean Mass Errors"),
                        renderImgSection(missedCleavages.plot(missedCleav_dict), 'Missed Cleavages'),
                        renderImgSection(RtcorrWithLibrary.plot(irt_dict), 'RT correlation with library'),
                        renderImgSection(libraryCoverage.plot(libCov_dict, lib), 'Coverage of Assay Library'), #Todo: library
                        renderImgSection(LibraryIntensityCorr.plot(libIntensity_dict), 'Library intensity correlation'),
                        renderImgSection(pyprophet_scores.plot(pp_score), 'Pyprophet Scores')
                        ])
    return sectionlist


def main():

    def valid_file(choices, fname):
        """check file extension and raise parser error"""
        ext = os.path.splitext(fname)[1][1:]
        if ext.lower() not in choices:
            parser.error("file doesn't end with one of {}".format(choices))
        return fname

    # add command line arguments
    parser = argparse.ArgumentParser(description="Create HTML report for Swatchworkflow, pyprophet and output")
    parser.add_argument('-p', '--pyprophet_file', help="output from pyprophet eiher as osw or legacy tsv file",
                        dest='pp_file', nargs='+', type=lambda s: valid_file(("tsv", "osw"), s), required=False)
    parser.add_argument('-s', '--swath_files', help="pyprophet tsv file", dest='swath_files', nargs='+',
                        type=lambda s: valid_file(("tsv", "osw"), s), required=False) # eiuther featureXML, tsv or osw
    parser.add_argument('-j', "--qc_json", help="input in json format", dest='input_json', type=lambda s: valid_file(("json"), s))
    parser.add_argument('-l', '--library', help='library file in tsv or pqp', dest='lib', type=lambda s: valid_file(("tsv", "pqp"), s), required=False)
    parser.add_argument('-o', '--out',  help='outfile name', default='report.html', dest='outfile', type=str,  required=False)
    # parse arguments
    args = parser.parse_args()


    # get the system path separator, (flexibility for windows and linux)
    separator = os.path.sep

    filedict = {}
    # add sections to list when the necessary dataframe is available below
    temp_vars = []


    dfdict = {}
    if args.swath_files is not None:
        swath_files = []
        #swath_dict = {}
        for i in args.swath_files:
            f = str.split(i, separator)[-1]
            swath_files.append(f)
            # read available files into dataframes
            if f.endswith("featureXML"):
                continue
            if f.endswith("tsv"):
                dfdict[f] = pd.read_csv(i, sep='\t')
            if f.endswith("osw"):
                # read all necessary tables into dictionary of dataframes:
                #{'file1.osw': {'feature': 'featuretable1', 'peptide': 'peptidetable1'},
                # 'file2.osw': {'feature': 'featuretable2', 'peptide': 'peptidetable2'}}
                subdict = {'feature': OSW2df(i, 'FEATURE'),
                           'featureMS2': OSW2df(i, 'FEATURE_MS2'),
                           'featureTransition': OSW2df(i, 'FEATURE_TRANSITION'),
                           'transition': OSW2df(i, 'TRANSITION'),  # only for summary table
                           'peptide': OSW2df(i, 'PEPTIDE'),
                           'protein': OSW2df(i, 'PROTEIN')}
                dfdict[f] = subdict
        filedict['swath files'] = swath_files
        #swath_dict={k: dfdict[k] for k in filedict['swath files']}
        #temp_vars.extend(plotsFromSwath(dfdict))


        #infotab = fileInfoTableOsw(infotab, swath_transition_dict, swath_peptide_dict, swath_protein_dict)

    if args.pp_file is not None:
        pp_files = []
        for pp_file in args.pp_file:
            # Todo maybe enable multiple pp files, osw and tsv?
            ppfile = str.split(pp_file, separator)[-1]
            pp_files.append(ppfile)
            if ppfile.endswith('tsv'):
                pp = pd.read_csv(pp_file, sep='\t')
                dfdict[ppfile] = pp
            if ppfile.endswith('osw'):
                subdict = {'feature': OSW2df(pp_file, 'FEATURE'),
                           'peptide': OSW2df(pp_file, 'PEPTIDE'),
                           'featureMS2': OSW2df(pp_file, 'FEATURE_MS2'),
                           'protein': OSW2df(pp_file, 'PROTEIN'),
                           'irt': irtDfFromSql(pp_file),
                           'featureTransition': OSW2df(pp_file, 'FEATURE_TRANSITION'),
                           'peptideScores': peptideScoreFromSql(pp_file),
                           'transition': OSW2df(pp_file, 'TRANSITION'), # only for summary table
                           'proteinScores': proteinScoreFromSql(pp_file)}

                dfdict[ppfile] = subdict

        filedict['pyprophet'] = pp_files
        print(filedict)

    # read library
    if args.lib is not None:
        libfile = str.split(args.lib, separator)[-1]
        filedict['library'] = libfile
        if libfile.lower().endswith('tsv'):
            lib = pd.read_csv(args.lib, sep='\t')
            dfdict[libfile] = lib
        if libfile.lower().endswith('pqp'):
            subdict = {'peptide': OSW2df(args.lib, 'PEPTIDE'),
                       'protein': OSW2df(args.lib, 'PROTEIN'),
                       'transition': OSW2df(args.lib, 'TRANSITION')}
            dfdict[libfile] = subdict

    print(filedict.keys())
    print(dfdict.keys())

    temp_vars.extend(plotsFromDfdict(dfdict, filedict))

    # restructure dict
    if args.swath_files is not None:
        min_length = len(args.swath_files)
    else:
        if args.pp_file is not None:
            min_length = len(args.pp_file)
        else:
            min_length = 1
    df = pd.DataFrame({k: pd.Series(v[:min_length]) for k, v in filedict.items()}).fillna('-')


    temp_vars.insert(0, topSection(df))
    temp_vars.insert(1, fileSummaryTable(sumTable(dfdict)))


    #temp_vars.insert(0, top_section(filedict))
    # templating
    # build dictionary of sections to include
    env = Environment(loader=FileSystemLoader('templates/'))  # or parh to template location
    template = env.get_template("base.html")
    template_vars = temp_vars
    # write out html string into report html file:
    html_out = template.render(items=template_vars)
    # weasy print rewires some more packages, GTK+
    #HTML(html_out).write_pdf(args.outfile, stlysheets=["templates/style.css"])
    with open(args.outfile, "w") as file:
        file.write(html_out)


if __name__ == "__main__":
    main()


# try:
#     import matplotlib
#     matplotlib.use('Agg')
#     from matplotlib.backends.backend_pdf import PdfPages
#     import matplotlib.pyplot as plt
# except ImportError:
#     plt = None