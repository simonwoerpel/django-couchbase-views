__author__ = 'simonwoerpel'

"""
Couchbase Connection
for convenience this should be imported like ...import CONNECTION as C
"""

from couchbase.bucket import Bucket
from .settings import CB_BUCKET, CB_HOST, CB_PASSWORD


def db_connection():
    return Bucket('http://%s/%s' % (CB_HOST, CB_BUCKET), password=CB_PASSWORD)

CONNECTION = db_connection()

