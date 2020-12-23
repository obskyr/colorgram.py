import timeit
import statistics

_setup = '''
from PIL import Image
num_colors = 6
img = Image.open('data/test.png')
img.load()
'''

_code = '''
import colorgram
colorgram.extract(img, num_colors)
'''
number = 20
repeats = 10
measures = timeit.repeat(setup=_setup, stmt=_code, number=number, repeat=repeats)

_mean = statistics.mean(measures) / number
_stdev = statistics.stdev(measures) / number

print('results: %0.6f (+/- %0.6f) sec.' % (_mean, _stdev))