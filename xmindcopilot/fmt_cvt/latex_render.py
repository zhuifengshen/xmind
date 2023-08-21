# -*- coding: utf-8 -*-

import os
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib.font_manager as mfm
from matplotlib import mathtext
from sympy import preview

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

def latex2img_sympy(text):
    preview(r'$$\int_0^1 e^x\,dx$$', viewer='file', filename='test.png', euler=False)