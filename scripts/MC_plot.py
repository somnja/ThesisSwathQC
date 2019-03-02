from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from plots import barplot
from scripts.stuff import img_to_html
'''plot missed cleavages, 
can only be don when one or multiple swath tsv were given
do one plot for each file
'''


def MC_plot(df):
    # prepare df:
    # - drop transitiosn tagged as decoys
    # - group by transitions group, or missed cleavages for one peptide will be counted multiple times
    plot_df = df[df.decoy == 0][['transition_group_id', 'MC']].drop_duplicates('transition_group_id').groupby('MC').count()
    # plot figure
    fig = barplot(df, 'Missed Cleavages', 'count', '# missed cleavages', labelcolor='black')
    return img_to_html(fig, 'MC1')


def sample_prep(dfdict):
    """Fill out section.html template"""
    # templating

    #splitpath = infiles.split("/")
    env = Environment(loader=FileSystemLoader('templates2/'))  #path to templates
    template = env.get_template("sample_prep.html")
    template_vars = {'id': 'section1',
                     'dataframe_head': df.head().to_html(),
                     'table_id': 'table1',
                     'p1': p1(df, splitpath[-1])}
    html_out = template.render(template_vars)
    return html_out