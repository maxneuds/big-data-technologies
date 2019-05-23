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
cb.n1ql_timeout = 3600

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
  q.timeout = 3600
  qres = cb.n1ql_query(q)
  for row in qres:
    print(row)


# query_result('select * from prak21 limit 100')
query_result('drop index prak21.movieIds;')
# query_result('create index movieIds on prak21(movieId);')
