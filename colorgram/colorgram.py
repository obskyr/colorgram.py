# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import division

import array
from collections import namedtuple
from PIL import Image

import sys
if sys.version_info[0] <= 2:
    range = xrange
    ARRAY_DATATYPE = b'l'
else:
    ARRAY_DATATYPE = 'l'

Rgb = namedtuple('Rgb', ('r', 'g', 'b'))
Hsl = namedtuple('Hsl', ('h', 's', 'l'))

class Color(object):
    def __init__(self, r, g, b, proportion):
        self.rgb = Rgb(r, g, b)
        self.proportion = proportion
    
    def __repr__(self):
        return "<colorgram.py Color: {}, {}%>".format(
            str(self.rgb), str(self.proportion * 100))

    @property
    def hsl(self):
        try:
            return self._hsl
        except AttributeError:
            self._hsl = Hsl(*hsl(*self.rgb))
            return self._hsl

def extract(f, number_of_colors):
    image = f if isinstance(f, Image.Image) else Image.open(f)
    if image.mode not in ('RGB', 'RGBA', 'RGBa'):
        image = image.convert('RGB')
    
    samples = sample(image)
    used = pick_used(samples)
    used.sort(key=lambda x: x[0], reverse=True)
    return get_colors(samples, used, number_of_colors)

def sample(image):
    top_two_bits = 0b11000000

    sides = 1 << 2 # Left by the number of bits used.
    cubes = sides ** 7

    samples = array.array(ARRAY_DATATYPE, (0 for _ in range(cubes)))
    width, height = image.size
    
    pixels = image.load()
    for y in range(height):
        for x in range(width):
            # Pack the top two bits of all 6 values into 12 bits.
            # 0bYYhhllrrggbb - luminance, hue, luminosity, red, green, blue.

            r, g, b = pixels[x, y][:3]
            h, s, l = hsl(r, g, b)
            # Standard constants for converting RGB to relative luminance.
            Y = int(r * 0.2126 + g * 0.7152 + b * 0.0722)

            # Everything's shifted into place from the top two
            # bits' original position - that is, bits 7-8.
            packed  = (Y & top_two_bits) << 4
            packed |= (h & top_two_bits) << 2
            packed |= (l & top_two_bits) << 0

            # Due to a bug in the original colorgram.js, RGB isn't included.
            # The original author tries using negative bit shifts, while in
            # fact JavaScript has the stupidest possible behavior for those.
            # By uncommenting these lines, "intended" behavior can be
            # restored, but in order to keep result compatibility with the
            # original the "error" exists here too. Add back in if it is
            # ever fixed in colorgram.js.

            # packed |= (r & top_two_bits) >> 2
            # packed |= (g & top_two_bits) >> 4
            # packed |= (b & top_two_bits) >> 6
            # print "Pixel #{}".format(str(y * width + x))
            # print "h: {}, s: {}, l: {}".format(str(h), str(s), str(l))
            # print "R: {}, G: {}, B: {}".format(str(r), str(g), str(b))
            # print "Y: {}".format(str(Y))
            # print "Packed: {}, binary: {}".format(str(packed), bin(packed)[2:])
            # print
            packed *= 4
            samples[packed]     += r
            samples[packed + 1] += g
            samples[packed + 2] += b
            samples[packed + 3] += 1
    return samples

def pick_used(samples):
    used = []
    for i in range(0, len(samples), 4):
        count = samples[i + 3]
        if count:
            used.append((count, i))
    return used

def get_colors(samples, used, number_of_colors):
    pixels = 0
    colors = []
    number_of_colors = min(number_of_colors, len(used))

    for count, index in used[:number_of_colors]:
        pixels += count

        color = Color(
            samples[index]     // count,
            samples[index + 1] // count,
            samples[index + 2] // count,
            count
        )

        colors.append(color)
    for color in colors:
        color.proportion /= pixels
    return colors

def hsl(r, g, b):
    # This looks stupid, but it's way faster than min() and max().
    if r > g:
        if b > r:
            most, least = b, g
        elif b > g:
            most, least = r, g
        else:
            most, least = r, b
    else:
        if b > g:
            most, least = b, r
        elif b > r:
            most, least = g, r
        else:
            most, least = g, b

    l = (most + least) >> 1

    if most == least:
        h = s = 0
    else:
        diff = most - least
        if l > 127:
            s = diff * 255 // (510 - most - least)
        else:
            s = diff * 255 // (most + least)
        
        if most == r:
            h = (g - b) * 255 // diff + (1530 if g < b else 0)
        elif most == g:
            h = (b - r) * 255 // diff + 510
        else:
            h = (r - g) * 255 // diff + 1020
        h //= 6
    
    return h, s, l

# Useful snippet for testing values:
# print "Pixel #{}".format(str(y * width + x))
# print "h: {}, s: {}, l: {}".format(str(h), str(s), str(l))
# print "R: {}, G: {}, B: {}".format(str(r), str(g), str(b))
# print "Y: {}".format(str(Y))
# print "Packed: {}, binary: {}".format(str(packed), bin(packed)[2:])
# print

# And on the JS side:
# var Y = ~~(img.data[i] * 0.2126 + img.data[i + 1] * 0.7152 + img.data[i + 2] * 0.0722);
# console.log("Pixel #" + i / img.channels);
# console.log("h: " + h[0] + ", s: " + h[1] + ", l: " + h[2]);
# console.log("R: " + img.data[i] + ", G: " + img.data[i + 1] + ", B: " + img.data[i + 2]);
# console.log("Y: " + Y);
# console.log("Packed: " + v + ", binary: " + (v >>> 0).toString(2));
# console.log();
