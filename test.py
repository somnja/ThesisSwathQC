from __future__ import print_function
import pandas as pd
import argparse
from jinja2 import Environment, FileSystemLoader
import os
import base64
from io import BytesIO
from scripts.handleOSW import OSW2df
from scripts.plotFromAny import mIDoverRT, mPWoverRT, libraryCorr, libCoverage, pltLibCoverage
from scripts.fromSwathTsv import mPlotMassError, mTwoDimHist, missedCleavages
from scripts.section1 import input_args_table
from scripts.descriptions import describeIDoverRT, describeMissedCleavages, describePWoverRT, describeLibraryCorr


loreipsum = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore " \
            "et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet " \
            "clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, " \
            "consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, " \
            "sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea" \
            " takimata sanctus est Lorem ipsum dolor sit amet"

def renderImgSection(figurehtml, imgid, sectionid, sectionh, description, templateFolder='templates/', templateFile='sectionImg.html'):
    """for goven html string of a figure, render into html template
    :return html string of template"""
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


def main():

    def valid_file(choices, fname):
        """check file extension and raise parser error"""
        ext = os.path.splitext(fname)[1][1:]
        if ext.lower() not in choices:
            parser.error("file doesn't end with one of {}".format(choices))
        return fname

    # add command line rguments
    parser = argparse.ArgumentParser(description="Create HTML report for Swatchworkflow, pyprophet and output")
    parser.add_argument('-p', help="pyprophet osw file", dest='input_pp_osw',  type=lambda s: valid_file(("osw"), s))
    parser.add_argument('-t',  help="pyprophet tsv file", dest='input_pp_tsv', type=lambda s: valid_file(("tsv"), s))
    parser.add_argument('-s', help='one or more swath tsv files', dest='input_swath_tsv', nargs='+')
    parser.add_argument('-o', help='one or more swath osw files', dest='input_swath_osw', nargs='+')
    parser.add_argument('-j', "--in_json", help="input in json format", dest='input_json', type=lambda s: valid_file(("json"), s))
    parser.add_argument('-l', '--library', help='library file in tsv format, not pqp', dest='lib', type=str, required=False)
    parser.add_argument('--out',  help='outfile name', dest='outfile', type=str,  required=False)
    # parse arguments
    args = parser.parse_args()

    argsdf = pd.DataFrame.from_dict(vars(args), orient='index')
    in_pp_osw = str.split(args.input_pp_osw, '\\')[-1]

    print(argsdf)
    # list of templyte varibales to loop ober, each contains as section
    # add sections to list when the necessary dataframe is available below
    temp_vars = []
    temp_vars.append(input_args_table(argsdf))
    # read available all files into dataframes, or dictionries of dataframes

    if args.input_swath_tsv is not None:
        count = 1
        swath_tsv_dict = {}
        for i in args.input_swath_tsv:
            n = 'swath_tsv' + str(count)
            swath_tsv_dict[n] = pd.read_csv(i, sep='\t')
            count += count
        """temp_vars.extend([renderImgSection(missedCleavages(swath_tsv_dict), 'mc_img', 'mc',
                                           'Missed Cleavages', describeMissedCleavages()),
                          renderImgSection(mIDoverRT(swath_tsv_dict, 'RT'), 'idoverrt_img', 'idoverrt',
                                           'ID over RT ', describeIDoverRT('tsv')),
                          renderImgSection(mPWoverRT(swath_tsv_dict, 'tsv'), 'pwoverrt_img', 'pwoverrt',
                                           'PeakWidth over RT ', describePWoverRT('tsv')),
                          renderImgSection(libraryCorr(swath_tsv_dict, 'tsv'), 'lib_corr_img', 'lib_corr',
                                           'Correlation with Library Intensity', describeLibraryCorr('tsv')),
                          renderImgSection(mPlotMassError(swath_tsv_dict), 'masserror_img', 'masserror',
                                           'Mean Mass Error', loreipsum),
                          renderImgSection(mTwoDimHist(swath_tsv_dict), 'masserror_2d_img', 'masserror_2d',
                                           '2D Histrogram of mean mass errors', loreipsum)
                          ])"""
    else:
        temp_vars.append(renderMissingSection('OpenSwathWorkflow tsv files. Masserrors and missed cleavagescan not be plotted'))

    if args.input_swath_osw is not None:
        count = 1
        # feature tables
        swath_osw_dict = {}
        # MS2 table
        swath_MS2_dict = {}
        swath_peptide_dict = {}
        for i in args.input_swath_osw:

            swath_osw_dict[n] = OSW2df(i, 'FEATURE')
            swath_MS2_dict[n] = OSW2df(i, 'FEATURE_MS2')
            swath_peptide_dict[n] = OSW2df(i, 'PEPTIDE')
            count += count

        temp_vars.extend([renderImgSection(mPWoverRT(swath_osw_dict, 'osw'), 'pwoverrt_img', 'pwoverrt',
                                           'PeakWidth over RT from OpenSwathWorkflow osw ', "}"),
                          renderImgSection(mIDoverRT(swath_osw_dict, 'EXP_RT'), 'idoverrt_img', 'idoverrt',
                                           'ID over RT from OpenSwathWorkflow osw', describeIDoverRT('osw')),
                          renderImgSection(libraryCorr(swath_MS2_dict, 'osw'), 'lib_corr_img', 'lib_corr',
                                           'Correlation with Library Intensity',
                                           ' plotted from OSW <br> library correlattion is one of many subscores calculated by OpenSwathWorkflow' )
                          ])

    if args.input_pp_tsv is not None:
        pptsv = pd.read_csv(args.input_pp_tsv, sep='\t')


        '''temp_vars.extend([renderImgSection(PWoverRT(pptsv), 'PWoverRTimg', 'PWoverRT',
                                           'Peak Width over Retention Time', 'some description'),
                          renderImgSection(IDoverRT(pptsv), 'IDoverRT_img1', 'IDoverRT',
                                           'ID over Retention Time', 'some description'),
                          renderImgSection(numOfTransitions(pptsv), 'numofT_img1', 'numOfT',
                                           'Count plot for Number of Transitions', 'some description'),
         ])'''

    if args.input_pp_osw is not None:
        # read feature table from osw file
        pposw = OSW2df(args.input_pp_osw, 'FEATURE')
    # read swath tsv files into dictionary
    if args.lib is not None:
        lib = pd.read_csv(args.lib, sep='\t')
        temp_vars.append(renderImgSection(pltLibCoverage(swath_peptide_dict, lib, pptsv, source='osw'), 'libcov_img1', 'lib_cov',
                                           'Library Coverage', loreipsum))

    else:
        temp_vars.append(
            renderMissingSection('no transitionslist in tsv format was provided.<br> Library coverage can not be plotted.'))


    # table fo input arguments at top of page




    # templating
    # build dictionary of sections to include
    env = Environment(loader=FileSystemLoader('templates2/'))  # or parh to template location
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
