#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

####
# Couchbase
####

import pymongo


# login

client = pymongo.MongoClient(
    "mongodb://faircastle.fbi.h-da.de",
    username='prak21',
    password='prak21',
    authSource='prak21'
)


def idx_drop(db):
  try:
    db.movies.drop_index('idx_title')
  except pymongo.errors.OperationFailure:
    pass
  try:
    db.moviesref.drop_index('idx_title')
  except pymongo.errors.OperationFailure:
    pass
  try:
    db.moviesref.drop_index('idx_movieid')
  except pymongo.errors.OperationFailure:
    pass
  try:
    db.ratings.drop_index('idx_movieid')
  except pymongo.errors.OperationFailure:
    pass


def idx_create(db):
  db.movies.create_index(
      [('title', pymongo.TEXT)],
      name='idx_title', default_language='english')
  db.moviesref.create_index(
      [('title', pymongo.TEXT)],
      name='idx_title', default_language='english')
  db.moviesref.create_index(
      [('movieId', pymongo.ASCENDING)],
      name='idx_movieid')
  db.ratings.create_index(
      [('movieId', pymongo.ASCENDING)],
      name='idx_movieid')


with client:
  db = client.prak21
  col = db.movies
  q = {"_id": 6365}
  qres = col.find(q, {"ratings": 1}).explain()
  print(qres["operationTime"])
  for x in qres:
    print(x)

# with client:
#   db = client.prak21
#   col = db.movies
#   idx_drop(db)
#   idx_create(db)
