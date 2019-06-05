#!/usr/bin/python3

import sys
import json

hstream = sys.stdin

# single key mapping
# out = []
key = 'SumRatings'

for line in hstream:
  movie = json.loads(line.strip())
  value = len(movie['ratings'])
  print('{}:{}'.format(key, value))
