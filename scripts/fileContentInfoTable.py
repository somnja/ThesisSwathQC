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
    template_vars = {'h': 'Input Files',
                     'file_table': tab,
                     'table_id': 'file_table'}
    html_out = template.render(template_vars)
    return html_out


# Todo: adjust for dfdict



def fileSummaryTable(sumTab):
    tab = sumTab.to_html()

    env = Environment(loader=FileSystemLoader('templates/'))  # path to templates
    template = env.get_template("topSection.html")
    template_vars = {'h': 'File summary',
                     'file_table': tab,
                     'table_id': 'file_table'}
    html_out = template.render(template_vars)
    return html_out



def sumTable(dfdict):

    sumTab = pd.DataFrame({'filename': [],
                          '#target_transitions': [],
                          '#peptides': [],
                          '#proteins': [],
                          '#decoy_transitions': [],
                          '#decoy_peptides': [],
                          '#decoy_proteins': []})

    for k, df in dfdict.items():
        if k.lower().endswith('tsv'):

            decoysdf = df[df['decoy'] == 1]
            temp_df = df[df['decoy'] == 0]
            nrows, ncols = df.shape
            sumTab = sumTab.append({'filename': k,
                              '#target_transitions': temp_df.loc[:, 'FullPeptideName'].count(),
                              '#peptides': len(list(set(temp_df['FullPeptideName']))),
                              '#proteins': len(list(set(temp_df['ProteinName']))),
                              '#decoy_transitions': decoysdf.loc[:, 'decoy'].count(),
                              '#decoy_peptides': len(list(set(decoysdf['FullPeptideName']))),
                              '#decoy_proteins': len(list(set(decoysdf['ProteinName'])))
                              }, ignore_index=True)
        if k.lower().endswith(('osw', 'pqp')):
            dfs = dfdict[k]

            transition = dfs['transition']
            peptide = dfs['peptide']
            protein = dfs['protein']

            sumTab = sumTab.append({'filename': k,
                                        '#target_transitions': transition[transition['DECOY'] == 0]['ID'].count(),
                                        '#peptides': len(list(set(peptide[peptide['DECOY']==0]['ID']))),
                                        '#proteins': len(list(set(protein[protein['DECOY']==0]['ID']))),
                                        '#decoy_transitions': transition[transition['DECOY'] == 1]['ID'].count(),
                                        '#decoy_peptides': len(list(set(peptide[peptide['DECOY']==1]['ID']))),
                                        '#decoy_proteins': len(list(set(protein[protein['DECOY']==1]['ID'])))
                                        }, ignore_index=True)

    return sumTab
