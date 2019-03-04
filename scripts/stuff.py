import base64
from io import BytesIO


def checkFilyType(key):
    if key.lower().endswith('osw'):
        return 'osw'
    if key.lower().endswith('tsv'):
        return 'tsv'
    if key.lower().endswith('featureXML'):
        return 'featureXML'


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
    html = '<img class="myImages" src="data:image/png;base64,{0}" width=100%>'.format(data_uri)
    return html


def colorPP(key, filedict):
    if key in filedict['pyprophet']:
        color = '#3a78a4'
    else:
        color = 'coral'
    return color