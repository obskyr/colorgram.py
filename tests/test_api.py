# -*- coding: utf-8 -*-

from colorgram import colorgram
from PIL import Image
import requests

def test_extract_from_file():
    colorgram.extract('data/test.png', 1)

def test_extract_from_image_object():
    image = Image.open('data/test.png')
    colors = colorgram.extract(image, 1)

def test_extract_from_url():
    url = 'https://camo.githubusercontent.com/ca5e835b6671e2eb15679c13af834927f3d4d26e/687474703a2f2f692e696d6775722e636f6d2f4265526561524d2e706e67'
    res = requests.get(url)
    colorgram.extract(res.content, 1)

def test_color_access():
    color = colorgram.Color(255, 151, 210, 0.15)

    assert color.rgb == (255, 151, 210)
    assert (color.rgb.r, color.rgb.g, color.rgb.b) == color.rgb

    assert color.hsl == (230, 255, 203)
    assert (color.hsl.h, color.hsl.s, color.hsl.l) == color.hsl

    assert color.proportion == 0.15
