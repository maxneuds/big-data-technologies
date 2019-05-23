#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

####
# Couchbase
####

import couchbase
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery

# login

cluster = Cluster('couchbase://silverhill.fbi.h-da.de')
authenticator = PasswordAuthenticator('prak21', 'prak21')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('prak21')
cb.n1ql_timeout = 3600

# analyze functions


def cb_index_create():
  q1 = 'create index movieIds on prak21(movieId);'
  q2 = 'create index titles on prak21(title);'
  query_result(q1)
  query_result(q2)


def cb_index_drop():
  q1 = N1QLQuery('drop index prak21.movieIds;')
  q2 = N1QLQuery('drop index prak21.titles;')
  try:
    cb.n1ql_query(q1).execute()
  except couchbase.exceptions.HTTPError:
    pass
  try:
    cb.n1ql_query(q2).execute()
  except couchbase.exceptions.HTTPError:
    pass


def query_result(string_query):
  q = N1QLQuery(string_query)
  q.timeout = 3600
  qres = cb.n1ql_query(q)
  for row in qres:
    print(row)


def query_time(string_query, repetitions):
  times = []
  q = N1QLQuery(string_query)
  q.timeout = 3600
  for _ in range(repetitions):
    qres = cb.n1ql_query(q).execute()
    time = qres.metrics['executionTime']
    # extract time we get times like 'x.xxs' or 'x.xxms'
    # s is seconds, ms is milliseconds
    format_letter = time[-2]
    if format_letter == 'm':
      times.append(round(float(time[:-2]), 2))
    else:
      times.append(round(float(time[:-1]) * 1000, 2))
  times = np.array(times)
  time_avg = np.round(np.mean(times), 0)
  time_std = np.round(np.std(times), 0)
  return(time_avg, time_std)

####
# Aufgabe 1
####


# run queries and collect times
n = 5
q1 = "select title from prak21 where title like '%Matrix%';"
q2 = "select ratings from prak21 where movieId = 6365;"
q3 = "select title, ratings from prak21 where movieId = 6365;"
cb_index_drop()
t1, std1 = query_time(q1, n)
t2, std2 = query_time(q2, n)
t3, std3 = query_time(q3, n)
times_noidx = np.array([t1, t2, t3])
std_noidx = np.array([std1, std2, std3])
cb_index_create()
t4, std4 = query_time(q1, n)
t5, std5 = query_time(q2, n)
t6, std6 = query_time(q3, n)
times_idx = np.array([t4, t5, t6])
std_idx = np.array([std4, std5, std6])

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
