# -*- coding: utf-8 -*-

import json
import os
import colorgram

# The goal of colorgram.py is not only to extract colors properly,
# but to extract the same colors as colorgram.js would.

def create_test(image_path, extractions_path, num_colors):
    def func():
        with open(extractions_path, 'r') as f:
            correct_colors = json.load(f)[str(num_colors)]
        colors = colorgram.extract(image_path, num_colors)
        assert len(colors) == num_colors
        
        for correct_color, color in zip(correct_colors, colors):
            assert tuple(correct_color[:3]) == color.rgb
            assert -0.01 < correct_color[3] - color.proportion < 0.01
    
    return func

test_1_color = create_test('data/test.png', 'data/test.json', 1)
test_12_colors = create_test('data/test.png', 'data/test.json', 12)
