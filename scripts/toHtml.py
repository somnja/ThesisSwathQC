import base64
from io import BytesIO


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





