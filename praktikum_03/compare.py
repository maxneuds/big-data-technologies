#!/bin/env python

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery

# login

cluster = Cluster('couchbase://silverhill.fbi.h-da.de')
authenticator = PasswordAuthenticator('prak21', 'prak21')
cluster.authenticate(authenticator)
cb = cluster.open_bucket('prak21')

# query

# simple commands
# cb.n1ql_query('CREATE PRIMARY INDEX ON bucket-name').execute()

# selections
q = N1QLQuery('SELECT * FROM prak21 where movieId < 100 limit 10;')
result = cb.n1ql_query(q)
for row in result:
  print(row)
