import cython

# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
# cython: nonecheck=False
# cython: language_level=3

@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.cdivision(True)
@cython.optimize.unpack_method_calls(True)
cdef int rgb_to_pack(int r, int g, int b):
    # declare variables
    cdef int most = 0
    cdef int least = 0
    cdef int diff = 0
    cdef int h = 0
    cdef int s = 0
    cdef int l = 0
    cdef int Y = 0

    cdef int top_two_bits = 0b11000000
    cdef int result = 0

    # extract HSL+Y - This looks stupid, but it's way faster than min() and max().
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

    Y = int(r * 0.2126 + g * 0.7152 + b * 0.0722)

    # return packed info
    # result = (Y & top_two_bits) << 4
    # result |= (h & top_two_bits) << 2
    # result |= (l & top_two_bits) << 0
    #
    # result *= 4

    return (((Y & top_two_bits) << 4) + ((h & top_two_bits) << 2) + (l & top_two_bits)) * 4
    # return result

@cython.wraparound(False)
@cython.boundscheck(False)
cpdef list sample(list pixels):
    cdef int top_two_bits = 0b11000000

    cdef int sides = 1 << 2  # 4 - Left by the number of bits used.

    cdef int cubes = sides ** 7

    cdef list samples = [0] * cubes

    for item in pixels:
        r = item[0]
        g = item[1]
        b = item[2]
        # Pack the top two bits of all 6 values into 12 bits.
        # 0bYYhhllrrggbb - luminance, hue, luminosity, red, green, blue.

        # Standard constants for converting RGB to relative luminance.
        # Y = int(r * 0.2126 + g * 0.7152 + b * 0.0722)

        # Everything's shifted into place from the top two
        # bits' original position - that is, bits 7-8.
        # packed = (Y & top_two_bits) << 4
        # packed |= (h & top_two_bits) << 2
        # packed |= (l & top_two_bits) << 0

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

        packed = rgb_to_pack(r,g,b)

        # packed = 0
        samples[packed] += r
        samples[packed + 1] += g
        samples[packed + 2] += b
        samples[packed + 3] += 1
    return samples


@cython.wraparound(False)
@cython.boundscheck(False)
@cython.nonecheck(False)
@cython.cdivision(True)
@cython.optimize.unpack_method_calls(True)
cpdef (int, int, int) hsl(int r, int g, int b):
    # declare variables
    cdef int most = 0
    cdef int least = 0
    cdef int diff = 0
    cdef int h = 0
    cdef int s = 0
    cdef int l = 0

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
