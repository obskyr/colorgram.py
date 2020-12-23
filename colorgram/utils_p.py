# -*- coding: utf-8 -*-

import array
import sys

if sys.version_info[0] <= 2:
    range = xrange
    ARRAY_DATATYPE = b'l'
else:
    ARRAY_DATATYPE = 'l'


def sample(pixels):
    top_two_bits = 0b11000000

    sides = 1 << 2  # Left by the number of bits used.
    cubes = sides ** 7

    samples = array.array(ARRAY_DATATYPE, (0 for _ in range(cubes)))

    for pixel in pixels:
        # Pack the top two bits of all 6 values into 12 bits.
        # 0bYYhhllrrggbb - luminance, hue, luminosity, red, green, blue.

        r, g, b = pixel[0], pixel[1], pixel[2]
        h, s, l = hsl(r, g, b)
        # Standard constants for converting RGB to relative luminance.
        Y = int(r * 0.2126 + g * 0.7152 + b * 0.0722)

        # Everything's shifted into place from the top two
        # bits' original position - that is, bits 7-8.
        packed = (Y & top_two_bits) << 4
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
        samples[packed] += r
        samples[packed + 1] += g
        samples[packed + 2] += b
        samples[packed + 3] += 1
    return samples


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
