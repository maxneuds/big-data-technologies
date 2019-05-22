#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt

####
# Couchbase
####

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery

# login

cluster = Cluster('couchbase://silverhill.fbi.h-da.de')
authenticator = PasswordAuthenticator('prak21', 'prak21')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('prak21')

# analyze functions


def cb_index_create():
  q1 = N1QLQuery('create index movieIds on prak21(movieId);')
  q2 = N1QLQuery('create index titles on prak21(title);')
  cb.n1ql_query(q1)
  cb.n1ql_query(q2)


def cb_index_drop():
  q1 = N1QLQuery('drop index prak21.movieIds;')
  q2 = N1QLQuery('drop index prak21.titles;')
  cb.n1ql_query(q1)
  cb.n1ql_query(q2)


def query_result(string_query):
  q = N1QLQuery(string_query)
  qres = cb.n1ql_query(q)
  for row in qres:
    print(row)


def query_time(string_query, repetitions):
  times = []
  q = N1QLQuery(string_query)
  for _ in range(4):
    qres = cb.n1ql_query(q)
    time = qres.metrics['executionTime']
    # cut the 's' from 'x.xxxxxs'
    times.append(round(float(time[:-1]), 2))
  times = np.array(times)
  time_avg = np.mean(times)
  time_std = np.std(times)
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
# expected outputs:
# times_noidx = np.array([9.4425, 9.2825, 9.36])
# std_noidx = np.array([0.10231691, 0.06299802, 0.12668859])
# times_idx = np.array([9.685, 9.235, 9.335])
# std_idx = np.array([0.78014422, 0.03570714, 0.10136567])

# visualize
ind = np.arange(len(times_noidx))  # the x locations for the groups
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, times_noidx, width,
                yerr=std_noidx, label='No Index')
rects2 = ax.bar(ind + width/2, times_idx, width, yerr=std_idx, label='Index')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Times')
ax.set_title('Times with and without index')
ax.set_xticks(ind)
ax.set_xticklabels(('Q1', 'Q2', 'Q3'))
ax.legend()

fig.tight_layout()

plt.show(block=True)
