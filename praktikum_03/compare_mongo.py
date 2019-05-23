#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

####
# MonoDB
####

import pymongo

# login

client = pymongo.MongoClient(
    "mongodb://faircastle.fbi.h-da.de",
    username='prak21',
    password='prak21',
    authSource='prak21'
)

# analyze functions


def mongo_idx_drop():
  with client:
    db = client.prak21
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


def mongo_idx_create():
  with client:
    db = client.prak21
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


def query_result(collection, dict_query):
  with client:
    db = client.prak21
    col = db[collection]
    qres = col.find(dict_query)
    for x in qres:
      print(x)


def query_time(collection, dict_query, dict_select, repetitions):
  times = []
  for _ in range(repetitions):
    with client:
      db = client.prak21
      col = db[collection]
      qres = col.find(dict_query, dict_select).explain()
      stats = qres["executionStats"]
      time = stats["executionTimeMillis"]
      times.append(time)
  times = np.array(times)
  time_avg = np.round(np.mean(times), 0)
  time_std = np.std(times)
  return(time_avg, time_std)

####
# Aufgabe 1
####


# run queries and collect times
n = 5
q1 = {"title": {"$regex": "Matrix"}}
q12 = {"$text": {"$search": "Matrix"}}
s1 = {"title": 1}
q2 = {"_id": 6365}
s2 = {"ratings": 1}
q3 = {"_id": 6365}
s3 = {"title": 1, "ratings": 1}
mongo_idx_drop()
t1, std1 = query_time('movies', q1, s1, n)
t2, std2 = query_time('movies', q2, s2, n)
t3, std3 = query_time('movies', q3, s3, n)
times_noidx = np.array([t1, t2, t3])
std_noidx = np.array([std1, std2, std3])
print(times_noidx)
print(std_noidx)
mongo_idx_create()
t4, std4 = query_time('movies', q12, s1, n)
t5, std5 = query_time('movies', q2, s2, n)
t6, std6 = query_time('movies', q3, s3, n)
times_idx = np.array([t4, t5, t6])
std_idx = np.array([std4, std5, std6])
print(times_idx)
print(std_idx)

# visualize
ind = np.arange(len(times_noidx))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, times_noidx, width,
                yerr=std_noidx, label='No Index')
rects2 = ax.bar(ind + width/2, times_idx, width, yerr=std_idx, label='Index')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('times in ms')
ax.set_title('times with and without index in ms')
ax.set_xticks(ind)
ax.set_xticklabels(('Q1', 'Q2', 'Q3'))
ax.legend()


def autolabel(rects, xpos='center'):
  ha = {'center': 'center', 'right': 'left', 'left': 'right'}
  offset = {'center': 0, 'right': 1, 'left': -1}

  for rect in rects:
    height = rect.get_height()
    ax.annotate('{}'.format(height),
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(offset[xpos]*3, 3),  # use 3 points offset
                textcoords="offset points",  # in both directions
                ha=ha[xpos], va='bottom')


autolabel(rects1, "left")
autolabel(rects2, "right")

fig.tight_layout()

plt.show(block=True)
