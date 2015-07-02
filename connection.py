__author__ = 'simonwoerpel'

"""
Couchbase Connection
for convenience this should be imported like ...import CONNECTION as C
"""

from couchbase.bucket import Bucket
from .settings import CONNECTION_STR


def db_connection():
    return Bucket(CONNECTION_STR)

CONNECTION = db_connection()

