from __future__ import print_function
import pandas as pd
import argparse
from jinja2 import Environment, FileSystemLoader
import os
import base64
from io import BytesIO
from scripts.handleOSW import OSW2df
from plots.plots import *
from scripts.section1 import *
from scripts.descriptions import *


loreipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore " \
            "et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet " \
            "clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, " \
            "consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, " \
            "sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea" \
            " takimata sanctus est Lorem ipsum dolor sit amet"

def renderImgSection(figurehtml, imgid, sectionid, sectionh, description, templateFolder='templates/', templateFile='sectionImg.html'):
    """for given html string of a figure, render into html template:
    place image in image div, beside descripion div, add id for image container and section
    :return html string of section"""

    env = Environment(loader=FileSystemLoader(templateFolder))  #path to templates; eg 'templates2/'
    template = env.get_template(templateFile) #"sample_prep.html"
    template_vars = {'id': sectionid,
                     'img_id': imgid,
                     'h4': sectionh,
                     'description': description,
                     'figure': figurehtml}
    html_out = template.render(template_vars)
    return html_out

def renderMissingSection(missinginput):
    html = '<dev class="sec"><h3>Missing input files</h3>The following input files were not specified: ' + missinginput +'. </dev>'
    return html


def img_to_html(figure):
    """
      @brief
      @param
      @return
      """
    buffer = BytesIO()
    figure.savefig(buffer, format='png')
    buffer.seek(0)

    data_uri = base64.b64encode(buffer.read()).decode('ascii')
    html = '<img class="myImages" src="data:image/png;base64,{0}" >'.format(data_uri)
    return html

def plotsFromSwathTsv(swath_tsv_dict):
    sectionlist = ['<h2>Plotting from SWATH tsv input files</h2>']

    sectionlist.extend([renderImgSection(pltMissedCleavages(swath_tsv_dict), 'mc_img', 'mc',
                         'Missed Cleavages', describeMissedCleavages()),
                      renderImgSection(pltIDoverRT(swath_tsv_dict), 'idoverrt_img', 'idoverrt',
                         'ID over RT ', describeIDoverRT('tsv')),
                      renderImgSection(pltPWoverRT(swath_tsv_dict), 'pwoverrt_img', 'pwoverrt',
                         'PeakWidth over RT ', describePWoverRT('tsv')),
                      renderImgSection(pltLibCorr(swath_tsv_dict), 'lib_corr_img', 'lib_corr',
                         'Correlation with Library Intensity', describeLibraryCorr('tsv')),
                      renderImgSection(pltMassError(swath_tsv_dict), 'masserror_img', 'masserror',
                         'Mean Mass Error', loreipsum),
                      renderImgSection(pltPWoverRT(swath_tsv_dict), 'pwoverrt_img', 'pwoverrt',
                                       'PeakWidth over RT ', describePWoverRT('tsv')),
                      #renderImgSection(pltTwoDimHist(swath_tsv_dict), 'masserror_2d_img', 'masserror_2d',
                       #                '2D Histrogram of mean mass errors', loreipsum)
                        ])

    return sectionlist

def plotsFromSwathOsw(swath_osw_dict, swath_MS2_dict):
    sectionlist = ['<h2>Plots from SWATH OSW files</h2>']
    sectionlist.extend([renderImgSection(pltPWoverRT(swath_osw_dict), 'pwoverrt_img', 'pwoverrt',
                                       'PeakWidth over RT from OpenSwathWorkflow osw ', loreipsum),
                      renderImgSection(pltIDoverRT(swath_osw_dict), 'idoverrt_img', 'idoverrt',
                                       'ID over RT from OpenSwathWorkflow osw', describeIDoverRT('osw')),
                      renderImgSection(pltLibCorr(swath_MS2_dict), 'lib_corr_img', 'lib_corr',
                                       'Correlation with Library Intensity',
                                       ' plotted from OSW <br> library correlation is one of many subscores calculated by OpenSwathWorkflow'),
                      #renderImgSection(pltIRTCorr(swath_osw_dict), 'irtcoorr_img', 'irt_corr',
                       #               'RT correlation', loreipsum)
                      ])
    return sectionlist

def plotsFromPpOsw():

    return 0


def plotsFromPpTsv(pptsv, pptsvfile):
    sectionlist = []
    sectionlist.extend([renderImgSection(pltNumOfTransitions({pptsvfile: pptsv}), 'numtransitions_img', 'num_transitions',
                                       'Number of transitions', describeNofTransitions()),
                       renderImgSection(pltIRTCorr({pptsvfile:pptsv}), 'irtcorr_pp_img', 'irt_cirr_pp',
                        'RT correlation', loreipsum)])

    '''temp_vars.extend([renderImgSection(PWoverRT(pptsv), 'PWoverRTimg', 'PWoverRT',
                                       'Peak Width over Retention Time', 'some description'),
                      renderImgSection(IDoverRT(pptsv), 'IDoverRT_img1', 'IDoverRT',
                                       'ID over Retention Time', 'some description'),
                      renderImgSection(numOfTransitions(pptsv), 'numofT_img1', 'numOfT',
                                       'Count plot for Number of Transitions', 'some description'),
     ])'''
    return sectionlist


def main():

    def valid_file(choices, fname):
        """check file extension and raise parser error"""
        ext = os.path.splitext(fname)[1][1:]
        if ext.lower() not in choices:
            parser.error("file doesn't end with one of {}".format(choices))
        return fname

    # add command line rguments
    parser = argparse.ArgumentParser(description="Create HTML report for Swatchworkflow, pyprophet and output")
    parser.add_argument('-po', '--pp_osw', help="pyprophet osw file", dest='input_pp_osw',  type=lambda s: valid_file(("osw"), s))
    parser.add_argument('-pt',  '--pp_tsv', help="pyprophet tsv file", dest='input_pp_tsv', type=lambda s: valid_file(("tsv"), s))
    parser.add_argument('-st', '--swath_tsvs', help='one or more swath tsv files', dest='input_swath_tsv', nargs='+')
    parser.add_argument('-so', '--swath_osws', help='one or more swath osw files', dest='input_swath_osw', nargs='+')
    parser.add_argument('-j', "--qc_json", help="input in json format", dest='input_json', type=lambda s: valid_file(("json"), s))
    parser.add_argument('-l', '--library', help='library file in tsv format, not pqp', dest='lib', type=str, required=False)
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
    s_osw = args.input_swath_osw is not None
    s_tsv = args.input_swath_tsv is not None
    pp_tsv = args.input_pp_tsv is not None
    pp_osw = args.input_pp_osw is not None
    library = args.lib is not None


    if s_tsv:
        # read in dataframe
        swath_tsv_dict = {}
        s_tsvfiles = []
        for i in args.input_swath_tsv:
            n = str.split(i, separator)[-1]
            s_tsvfiles.append(n)
            swath_tsv_dict[n] = pd.read_csv(i, sep='\t')
        filedict['swath tsv files'] = s_tsvfiles

        infotab = fileInformationTable(infotab, swath_tsv_dict)
    # plot from tsv first if available
    if s_tsv and not s_osw:
        temp_vars.extend(plotsFromSwathTsv(swath_tsv_dict))

    if s_tsv and s_osw:
        # read in osw file names first, in case s_osw loop does not get enterd
        s_oswfiles = []
        for i in args.input_swath_osw:
            n = str.split(i, separator)[-1]
            s_oswfiles.append(n)
        filedict['swath osw'] = s_oswfiles
        if len(args.input_swath_tsv) >= len(args.input_swath_osw):
            swath_osw_dict = {}
            swath_MS2_dict = {}
            swath_peptide_dict = {}
            swath_protein_dict = {}
            swath_transition_dict = {}
            for i in args.input_swath_osw:
                n = str.split(i, separator)[-1]
                swath_osw_dict[n] = OSW2df(i, 'FEATURE')
                swath_MS2_dict[n] = OSW2df(i, 'FEATURE_MS2')
                swath_peptide_dict[n] = OSW2df(i, 'PEPTIDE')
                swath_protein_dict[n] = OSW2df(i, 'PROTEIN')
                swath_transition_dict[n] = OSW2df(i, 'TRANSITION')

            temp_vars.extend(plotsFromSwathOsw(swath_osw_dict, swath_MS2_dict))


    if s_osw and not s_tsv:
        # read in osw dataframes
        # feature tables
        swath_osw_dict = {}
        swath_MS2_dict = {}
        swath_peptide_dict = {}
        swath_protein_dict = {}
        swath_transition_dict = {}
        for i in args.input_swath_osw:
            n = str.split(i, separator)[-1]
            swath_osw_dict[n] = OSW2df(i, 'FEATURE')
            swath_MS2_dict[n] = OSW2df(i, 'FEATURE_MS2')
            swath_peptide_dict[n] = OSW2df(i, 'PEPTIDE')
            swath_protein_dict[n] = OSW2df(i, 'PROTEIN')
            swath_transition_dict[n] = OSW2df(i, 'TRANSITION')

        temp_vars.extend(plotsFromSwathOsw(swath_osw_dict, swath_MS2_dict))
        infotab = fileInfoTableOsw(infotab, swath_transition_dict, swath_peptide_dict, swath_protein_dict)


    if pp_tsv:
        pptsvfile = str.split(args.input_pp_tsv, separator)[-1]
        pptsv = pd.read_csv(args.input_pp_tsv, sep='\t')
        filedict['pyprophet tsv'] = [pptsvfile]
        temp_vars.extend(plotsFromPpTsv(pptsv, pptsvfile))

        infotab = fileInformationTable(infotab, {pptsvfile: pptsv})

    if pp_tsv and pp_osw:
        pposwfile = str.split(args.input_pp_osw, separator)[-1]
        filedict['pyprophet osw'] = [pposwfile]

    else:
        if pp_osw:
            pposwfile = str.split(args.input_pp_osw, separator)[-1]
            # read feature table from osw file
            pposw = OSW2df(args.input_pp_osw, 'FEATURE')
            temp_vars.extend(plotsFromPpOsw(pposw, pposwfile))
            infotab = fileInfoTableOsw(infotab, {pposwfile, pposw})

    # plot library coverage, if library is provided
    if library:
        filedict['library'] = [str.split(args.lib, separator)[-1]]
        if args.lib.lower().endswith('.pqp'):
            lib = OSW2df(args.lib, 'PEPTIDE')
        if args.lib.lower().endswith('.tsv'):
            lib = pd.read_csv(args.lib, sep='\t')
        # plot library coverage
        if pp_tsv:
            pp = pptsv
        else:
            if pp_osw:
                pposw_peptide = OSW2df(args.input_pp_osw, 'PEPTIDE')
                pp = pposw_peptide

        if s_tsv and not s_osw:
            temp_vars.append(
                renderImgSection(pltLibCoverage(swath_tsv_dict, lib, pp, source='tsv'), 'libcov_img1', 'lib_cov',
                                 'Library Coverage', describeLibCoverage('tsv')))
        if s_tsv and s_osw:
            if len(args.input_swath_tsv) >= len(args.input_swath_osw):
                temp_vars.append(
                    renderImgSection(pltLibCoverage(swath_tsv_dict, lib, pp, source='tsv'), 'libcov_img1', 'lib_cov','Library Coverage', describeLibCoverage('tsv')))
        if s_osw and not s_tsv:
            swath_peptide_dict = {}
            for i in args.input_swath_osw:
                n = str.split(i, separator)[-1]
                swath_peptide_dict[n] = OSW2df(i, 'PEPTIDE')
            temp_vars.append(renderImgSection(pltLibCoverage(swath_peptide_dict, lib, pp, source='osw'),
                                          'libcov_img1', 'lib_cov', 'Library Coverage', describeLibCoverage('osw')))


    else:
        temp_vars.append(
            renderMissingSection('no transitionslist in tsv format was provided.<br> Library coverage can not be plotted.'))

    print('filedict: ,' , filedict)


    # restructure dict
    min_length = 3
    #min_length = max(len(elem) for elem in [args.input_swath_tsv, args.input_swath_osw])



    df = pd.DataFrame({k: pd.Series(v[:min_length]) for k, v in filedict.items()}).fillna('-')
    print(df.T)

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
