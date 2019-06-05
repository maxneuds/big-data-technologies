#!/usr/bin/python3

import sys

hstream = sys.stdin

# single key mapping
counter = {}

for line in hstream:
  line = line.strip()
  key, value = line.split(':')

  # convert value to int
  try:
    count = int(value)
  except ValueError:
    continue

  # count
  try:
    counter[key] = counter[key] + count
  except:
    counter[key] = count

for key in counter.keys():
  print('{}: {}'.format(key, counter[key]))
