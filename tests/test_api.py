# -*- coding: utf-8 -*-

import colorgram
from PIL import Image

def test_extract_from_file():
    colorgram.extract('data/test.png', 1)

def test_extract_from_image_object():
    image = Image.open('data/test.png')
    colorgram.extract(image, 1)

def test_color_access():
    color = colorgram.Color(255, 151, 210, 0.15)

    assert color.rgb == (255, 151, 210)
    assert (color.rgb.r, color.rgb.g, color.rgb.b) == color.rgb

    assert color.hsl == (230, 255, 203)
    assert (color.hsl.h, color.hsl.s, color.hsl.l) == color.hsl

    assert color.proportion == 0.15
