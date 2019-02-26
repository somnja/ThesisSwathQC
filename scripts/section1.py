from jinja2 import Environment, FileSystemLoader
import pandas as pd

'''reutrn html string of section 1
'''

def check_pp_tric(df):
    """for a given dataframe check the expected number of columns and colum names
    and determine, if dataframe is from TRIC or PyProphet tsv file
    return a string: ['pyprophet', 'TRIC']"""
    cols = df.columns
    if 'align_origfilename' in cols and len(cols) == 36:
        return "TRIC"
    if len(cols) == 33:
        return "PyProphet"
    else:
        return "Neither PyProphet nor TRIC "


def topSection(df):
    """Fill out section.html template"""
    #argsdf = pd.DataFrame.from_dict(filedict, orient='index')

    #pd.set_option('display.max_colwidth', 800)
    tab = df.to_html()

    env = Environment(loader=FileSystemLoader('templates/'))  # path to templates
    template = env.get_template("topSection.html")
    template_vars = {'h': 'Command line arguments',
                     'file_table': tab,
                     'table_id': 'file_table'}
    html_out = template.render(template_vars)
    return html_out


def fileInformationTable(info_tab, dfdict, decoyCol='decoy'):
    """
    for tsv file dict like swath_tsv_dict or swath_osw_dict
    for osw, other tables are needed
    :param dfdict:
    :param decoyCol:
    :return: pandas dataframe
    """
    """df_table = pd.DataFrame({'filename': [],
                          '#rows': [],
                          '#cols': [],
                          '#targt_transitions': [],
                          '#peptides': [],
                          '#proteins': [],
                          '#decoy_transitions': [],
                          '#decoy_peptides': [],
                          '#decoy_proteins': []
                          })"""

    for k, df in dfdict.items():

        decoysdf = df[df[decoyCol] == 1]
        temp_df = df[df[decoyCol] == 0]
        nrows, ncols = df.shape
        info_tab = info_tab.append({'filename': k,
                              '#rows': nrows,
                              '#cols': ncols,
                              '#target_transitions': temp_df.loc[:, 'FullPeptideName'].count(),
                              '#peptides': len(list(set(temp_df['FullPeptideName']))),
                              '#proteins': len(list(set(temp_df['ProteinName']))),
                              '#decoy_transitions': decoysdf.loc[:, decoyCol].count(),
                              '#decoy_peptides': len(list(set(decoysdf['FullPeptideName']))),
                              '#decoy_proteins': len(list(set(decoysdf['ProteinName'])))
                              }, ignore_index=True)
    return info_tab

def fileInfoTableOsw(info_tab, transition_dict, peptide_dict, protein_dict):
    temp_dict = {}
    l_nrows = []
    l_ncols = []
    l_filename = []
    l_decoy_t = []
    l_target_t = []
    l_peptides = []
    l_proteins =[]
    l_decoy_peptides = []
    l_decoy_proteins = []
    for k, df in transition_dict.items():
        decoysdf = df[df['DECOY'] == 1]
        targetdf = df[df['DECOY'] == 0]
        nrows, ncols = df.shape
        l_nrows.append(nrows)
        l_ncols.append(ncols)
        l_filename.append(k)
        l_decoy_t.append(decoysdf['ID'].count())
        l_target_t.append(targetdf['ID'].count())
    for k, df in peptide_dict.items():
        decoysdf = df[df['DECOY'] == 1]
        targetdf = df[df['DECOY'] == 0]
        l_peptides.append(len(list(set(targetdf['ID']))))
        l_decoy_peptides.append(len(list(set(decoysdf['ID']))))

    for k , df in protein_dict.items():
        decoysdf = df[df['DECOY'] == 1]
        targetdf = df[df['DECOY'] == 0]
        l_proteins.append(len(list(set(targetdf['ID']))))
        l_decoy_proteins.append(len(list(set(decoysdf['ID']))))

    info_tab = info_tab.append({'filename': l_filename,
                                '#rows': l_nrows,
                                '#cols': l_ncols,
                                '#target_transitions': l_target_t,
                                '#peptides': l_peptides,
                                '#proteins': l_proteins,
                                '#decoy_transitions': l_decoy_t,
                                '#decoy_peptides': l_decoy_peptides,
                                '#decoy_proteins': l_decoy_proteins
                                }, ignore_index=True)
    return info_tab










def fileSummaryTable(df):
    tab = df.to_html()

    env = Environment(loader=FileSystemLoader('templates/'))  # path to templates
    template = env.get_template("topSection.html")
    template_vars = {'h': 'File summary',
                     'file_table': tab,
                     'table_id': 'file_table'}
    html_out = template.render(template_vars)
    return html_out



