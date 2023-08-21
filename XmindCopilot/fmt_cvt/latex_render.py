# -*- coding: utf-8 -*-

import os
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.font_manager as mfm
from matplotlib import mathtext
import requests
import tempfile
from ..utils import generate_id

TEMP_DIR = tempfile.gettempdir()

# DEPRECATED
def latex2img(text, size=32, color=(0.0, 0.0, 0.0), out=None, **kwds):
    """
    Convert LaTeX Mathematical Formulas to Images using mathtext

    :param text: Text string containing mathematical formulas enclosed between two dollar signs
    :param size: Font size, integer, default is 32
    :param color: Color, tuple of three floating-point values in the range [0, 1], default is black
    :param out: File name, only supports filenames with the .png extension. If None, a PIL image object will be returned.
    :param kwds: Keyword arguments
                dpi: Output resolution in dots per inch (DPI), default is 72
                family: System-supported font, None for the current default font
                weight: Stroke weight, options include: normal (default), light, and bold
    """

    assert out is None or os.path.splitext(
        out)[1].lower() == '.png', 'Only supports filenames with the .png extension'

    for key in kwds:
        if key not in ['dpi', 'family', 'weight']:
            raise KeyError('key is not supported:%s' % key)

    dpi = kwds.get('dpi', 72)
    family = kwds.get('family', None)
    weight = kwds.get('weight', 'normal')

    bfo = BytesIO()  # file-like object
    prop = mfm.FontProperties(family=family, size=size, weight=weight)
    mathtext.math_to_image(text, bfo, prop=prop, dpi=dpi)
    im = Image.open(bfo)

    r, g, b, a = im.split()
    r, g, b = 255-np.array(r), 255-np.array(g), 255-np.array(b)
    a = r/3 + g/3 + b/3
    r, g, b = r*color[0], g*color[1], b*color[2]

    im = np.dstack((r, g, b, a)).astype(np.uint8)
    im = Image.fromarray(im)

    if out is None:
        return im
    else:
        im.save(out)
        # print('File is saved to %s' % out)


def latex2img_web(expression, output_file=None, padding=10, image_format='png', verbose=False):
    """
    Convert LaTeX Mathematical Formulas to Images using mathtext

    :param expression: Text string containing mathematical formulas (NOT enclosed between two dollar signs)
    :param output_file: File name, only supports filenames with the .png extension. If None, a PIL image object will be returned.
    :param padding: Padding, integer, default is 10
    :param image_format: Image format, string, default is 'png'
    :param verbose: Whether to print verbose information, boolean, default is False
    :return: File path of the generated image
    """
    # base_url = "https://tools.timodenk.com"
    base_url = "http://localhost:3000"
    expression = expression.replace("$", "")  # Remove dollar signs
    endpoint = f"/api/tex2img/{expression}"
    query_params = {'padding': padding, 'format': image_format}

    vprint = print if verbose else lambda *a, **k: None
    
    response = requests.get(f"{base_url}{endpoint}", params=query_params, verify=False)

    if response.status_code == 200:
        content_type = response.headers['Content-Type']
        if 'svg' in content_type:
            file_extension = 'svg'
        elif 'jpeg' in content_type:
            file_extension = 'jpg'
        else:
            file_extension = image_format
        if output_file is None:
            print(TEMP_DIR)
            output_file = os.path.join(TEMP_DIR, generate_id() + f".{file_extension}")
        with open(output_file, 'wb') as f:
            f.write(response.content)
        vprint(f"Equation rendered and saved as {output_file}")
        return output_file
    elif response.status_code == 414:
        vprint("Request-URI Too Long: The expression exceeded the maximum length")
    elif response.status_code == 500:
        vprint("Internal Server Error: Conversion failed due to invalid TeX code")
    else:
        vprint(f"An error occurred with status code: {response.status_code}")


