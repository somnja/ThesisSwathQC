from __future__ import print_function
import argparse
import os
import base64
from io import BytesIO
from scripts.handleOSW import OSW2df
from plots import PeakWidthOverRT, IDoverRT, numOfTransitions
from scripts.section1 import *
from scripts.descriptions import *

#plt.rcParams.update({'font.size': 16})

# text filler for now
loreipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore " \
            "et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet " \
            "clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, " \
            "consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, " \
            "sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea" \
            " takimata sanctus est Lorem ipsum dolor sit amet"


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


def renderImgSection(figurehtml, sectionid, header, description, templateFolder='templates/', templateFile='sectionImg.html'):
    """
    render section with plot and plot description into html string with template
    :param figurehtml: html formatted plot
    :param sectionid: id of section
    :param header: section title
    :param description: html formatted string, description of the image
    :param templateFolder:
    :param templateFile:
    :return: section html as string
    """

    env = Environment(loader=FileSystemLoader(templateFolder))  #path to templates; eg 'templates2/'
    template = env.get_template(templateFile) #"sample_prep.html"
    template_vars = {'id': sectionid,
                     'h': header,
                     'description': description,
                     'figure': figurehtml}
    html_out = template.render(template_vars)
    return html_out
def renderImgSectionNew(figureAndDescription, header, templateFolder='templates/', templateFile='sectionImg.html'):

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

#def renderMissingSection(missinginput):
 #   html = '<dev class="sec"><h3>Missing input files</h3>The following input files were not specified: ' + missinginput +'. </dev>'
 #   return html




def plotsFromSwathTsv(swath_tsv_dict):
    sectionlist = ['<h2>Plotting from SWATH tsv input files</h2>']
    return sectionlist
#
#     sectionlist.extend([renderImgSection(pltMissedCleavages(swath_tsv_dict),  'mc', 'Missed Cleavages', describeMissedCleavages()),
#                       renderImgSection(pltIDoverRT(swath_tsv_dict), 'idoverrt', 'ID over RT ', describeIDoverRT('tsv')),
#                       renderImgSection(pltPWoverRT(swath_tsv_dict),  'pwoverrt', 'PeakWidth over RT ', describePWoverRT('tsv')),
#                       renderImgSection(pltLibCorr(swath_tsv_dict), 'lib_corr', 'Correlation with Library Intensity', describeLibraryCorr('tsv')),
#                       renderImgSection(pltMassError(swath_tsv_dict),  'masserror', 'Mean Mass Error', loreipsum),
#                       renderImgSection(pltPWoverRT(swath_tsv_dict),  'pwoverrt', 'PeakWidth over RT ', describePWoverRT('tsv'))
#                         ])
#



def plotsFromSwathOsw(feature_dict, featureTransition_dict, pp_dict):
    sectionlist = ['<h2>Plots from SWATH OSW files</h2>']
    sectionlist.extend([renderImgSectionNew(PeakWidthOverRT.plot(feature_dict), 'PeakWidth over RT'),
                        renderImgSectionNew(IDoverRT.plot(feature_dict), 'ID over RT'),
                        renderImgSectionNew(numOfTransitions.plot(featureTransition_dict), 'Number of Transitions')
                      ])
    return sectionlist


def plotsFromSwath(swath_dict):

    N = len(swath_dict)
    keys = swath_dict.keys()
    if list(swath_dict.keys())[0].lower().endswith('tsv'):
        return plotsFromSwathTsv()

    if list(keys)[0].lower().endswith('osw'):
        # unpack dict of dicts
        keyindex = zip(range(N), keys)
        feature = {}
        featureMS2 = {}
        featureTransition = {}
        for n, key in keyindex:
            print(n)
            print(key)
            dfs = swath_dict[key]
            feature[key] = dfs['feature']
            featureMS2[key] = dfs['featureMS2']
            featureTransition[key] = dfs['featureTransition']
        return plotsFromSwathOsw(feature, featureTransition)


def plotsFromDfdict(dfdict, filedict):
    sectionlist = []
    overRT_dict = {}
    numOfTransitions_dict = {}
    swath_dict = {}
    pp_dict = {}

    keys = dfdict.keys()

    if filedict['swath files'][0].lower().endswith('tsv'):
        swath_dict = {k: dfdict[k] for k in filedict['swath files']}
        overRT_dict.update(swath_dict)
        numOfTransitions_dict.update(swath_dict)
    if filedict['swath files'][0].lower().endswith('osw'):
        # unpack dict of dicts
        keyindex = zip(range(len(filedict['swath files'])), keys)
        swath_feature = {}
        swath_featureMS2 = {}
        swath_featureTransition = {}
        for n, key in keyindex:
            print(n)
            print(key)
            dfs = dfdict[key]
            swath_feature[key] = dfs['feature']
            swath_featureMS2[key] = dfs['featureMS2']
            swath_featureTransition[key] = dfs['featureTransition']
        overRT_dict.update(swath_feature)
        numOfTransitions_dict.update(swath_featureTransition)
    if filedict['pyprophet'][0].lower().endswith('tsv'):
        pp_dict = {k: dfdict[k] for k in filedict['pyprophet']}
        overRT_dict.update(pp_dict)
        numOfTransitions_dict.update(pp_dict)
    if filedict['pyprophet'][0].lower().endswith('osw'):
        key = filedict['pyprophet'][0]
        dfs = dfdict[key]
        pp_feature = {key: dfs['feature']}
        pp_peptide = {key: dfs['peptide']}
        pp_featureTransition = {key: dfs['featureTransition']}
        overRT_dict.update(pp_feature)
        numOfTransitions_dict.update(pp_featureTransition)
    sectionlist.extend([renderImgSectionNew(PeakWidthOverRT.plot(overRT_dict), 'PeakWidth over RT'),
                        renderImgSectionNew(IDoverRT.plot(overRT_dict), 'ID over RT'),
                        renderImgSectionNew(numOfTransitions.plot(numOfTransitions_dict), 'Number of Transitions')
                        ])
    return sectionlist


def plotsFromPpOsw():
    sectionlist = []

    return sectionlist

#
# def plotsFromPpTsv(pptsv, pptsvfile):
#     sectionlist = []
#     sectionlist.extend([renderImgSection(pltNumOfTransitions({pptsvfile: pptsv}), 'numtransitions_img', 'num_transitions',
#                                        'Number of transitions', describeNofTransitions()),
#                        renderImgSection(pltIRTCorr({pptsvfile:pptsv}), 'irtcorr_pp_img', 'irt_cirr_pp',
#                         'RT correlation', loreipsum)])
#
#     '''temp_vars.extend([renderImgSection(PWoverRT(pptsv), 'PWoverRTimg', 'PWoverRT',
#                                        'Peak Width over Retention Time', 'some description'),
#                       renderImgSection(IDoverRT(pptsv), 'IDoverRT_img1', 'IDoverRT',
#                                        'ID over Retention Time', 'some description'),
#                       renderImgSection(numOfTransitions(pptsv), 'numofT_img1', 'numOfT',
#                                        'Count plot for Number of Transitions', 'some description'),
#      ])'''
#     return sectionlist


def main():

    def valid_file(choices, fname):
        """check file extension and raise parser error"""
        ext = os.path.splitext(fname)[1][1:]
        if ext.lower() not in choices:
            parser.error("file doesn't end with one of {}".format(choices))
        return fname

    # add command line rguments
    parser = argparse.ArgumentParser(description="Create HTML report for Swatchworkflow, pyprophet and output")
    parser.add_argument('-p', '--pyprophet_file', help="output from pyprophet eiher as osw or legacy tsv file", dest='pp_file')
    parser.add_argument('-s', '--swath_files', help="pyprophet tsv file", dest='swath_files', nargs='+') # eiuther featureXML, tsv or osw
    parser.add_argument('-j', "--qc_json", help="input in json format", dest='input_json', type=lambda s: valid_file(("json"), s))
    parser.add_argument('-l', '--library', help='library file in tsv or pqp', dest='lib', type=str, required=False)
    parser.add_argument('-o', '--out',  help='outfile name', default='report.html', dest='outfile', type=str,  required=False)
    # parse arguments
    args = parser.parse_args()


    # get the system path separator, (flexibility for windows and linux)
    separator = os.path.sep

    filedict = {}
    # add sections to list when the necessary dataframe is available below
    temp_vars = []

    infotab = pd.DataFrame({'filename': [],  '#rows': [], '#cols': [], '#target_transitions': [],
                             '#peptides': [], '#proteins': [],
                             '#decoy_transitions': [], '#decoy_peptides': [], '#decoy_proteins': []})
#
    # file available ?

    library = args.lib is not None
    swaths = args.swath_files is not None

    dfdict = {}
    if swaths:
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
                plotsFromSwathTsv(dfdict)
            if f.endswith("osw"):
                # read all necessary tables into dictionary of dataframes:
                #{'file1.osw': {'feature': 'featuretable1', 'peptide': 'peptidetable1'},
                # 'file2.osw': {'feature': 'featuretable2', 'peptide': 'peptidetable2'}}
                subdict = {'feature': OSW2df(i, 'FEATURE'),
                           'featureMS2': OSW2df(i, 'FEATURE_MS2'),
                           'featureTransition': OSW2df(i, 'FEATURE_TRANSITION'),
                           'protein': OSW2df(i, 'PROTEIN')}
                dfdict[f] = subdict
        filedict['swath files'] = swath_files
        #swath_dict={k: dfdict[k] for k in filedict['swath files']}
        #temp_vars.extend(plotsFromSwath(dfdict))


        #infotab = fileInfoTableOsw(infotab, swath_transition_dict, swath_peptide_dict, swath_protein_dict)

    if args.pp_file is not None:
        # Todo maybe enable multiple pp files, osw and tsv?
        pp_dict = {}
        ppfile = str.split(args.pp_file, separator)[-1]
        if ppfile.endswith('tsv'):
            pp = pd.read_csv(args.pp_file, sep='\t')
            dfdict[ppfile] = pp
        if ppfile.endswith('osw'):
            subdict = {'feature': OSW2df(args.pp_file, 'FEATURE'),
                       'peptide': OSW2df(args.pp_file, 'PEPTIDE'),
                       'featureTransition': OSW2df(args.pp_file, 'FEATURE_TRANSITION')}
            dfdict[ppfile] = subdict

        filedict['pyprophet'] = [ppfile]

    # read library
    if args.lib is not None:
        libfile = str.split(args.lib, separator)[-1]
        filedict['library'] = libfile
        if libfile.endswith('tsv'):
            lib = pd.read_csv(args.lib, sep='\t')
            dfdict[libfile] = lib
        if libfile.endswith('pqp'):
            #subdict = {'peptide': OSW2df(args.lib, 'PEPTIDE')}
            lib = OSW2df(args.lib, 'PEPTIDE')
            dfdict[ppfile] = lib

    print(dfdict.keys())

    temp_vars.extend(plotsFromDfdict(dfdict, filedict))

    #         infotab = fileInfoTableOsw(infotab, {pposwfile, pposw})

    # # plot library coverage, if library is provided
    # if library:
    #     filedict['library'] = [str.split(args.lib, separator)[-1]]
    #     if args.lib.lower().endswith('.pqp'):
    #         lib = OSW2df(args.lib, 'PEPTIDE')
    #     if args.lib.lower().endswith('.tsv'):
    #         lib = pd.read_csv(args.lib, sep='\t')
    #     # plot library coverage
    #     if pp_tsv:
    #         pp = pptsv
    #     else:
    #         if pp_osw:
    #             pposw_peptide = OSW2df(args.input_pp_osw, 'PEPTIDE')
    #             pp = pposw_peptide
    #
    #     if s_tsv and not s_osw:
    #         temp_vars.append(
    #             renderImgSection(pltLibCoverage(swath_dict, lib, pp, source='tsv'), 'libcov_img1', 'lib_cov',
    #                              'Library Coverage', describeLibCoverage('tsv')))
    #     if s_tsv and s_osw:
    #         if len(args.input_swath_tsv) >= len(args.input_swath_osw):
    #             temp_vars.append(
    #                 renderImgSection(pltLibCoverage(swath_dict, lib, pp, source='tsv'), 'libcov_img1', 'lib_cov','Library Coverage', describeLibCoverage('tsv')))
    #     if s_osw and not s_tsv:
    #         swath_peptide_dict = {}
    #         for i in args.input_swath_osw:
    #             n = str.split(i, separator)[-1]
    #             swath_peptide_dict[n] = OSW2df(i, 'PEPTIDE')
    #         temp_vars.append(renderImgSection(pltLibCoverage(swath_peptide_dict, lib, pp, source='osw'),
    #                                       'libcov_img1', 'lib_cov', 'Library Coverage', describeLibCoverage('osw')))


    #else:
     #   temp_vars.append(
      #      renderMissingSection('no transitionslist in tsv format was provided.<br> Library coverage can not be plotted.'))

    print('filedict: ,' , filedict)


    # restructure dict
    min_length = len(args.swath_files)
    #min_length = max(len(elem) for elem in [args.input_swath_tsv, args.input_swath_osw])



    df = pd.DataFrame({k: pd.Series(v[:min_length]) for k, v in filedict.items()}).fillna('-')


    temp_vars.insert(0, topSection(df))
    temp_vars.insert(1, fileSummaryTable(infotab))


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
