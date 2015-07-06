__author__ = 'simonwoerpel'

"""
Couchbase Settings
"""


from django.conf import settings


CB = settings.COUCHBASE

CB_HOST = CB['HOST'] if 'HOST' in CB else 'localhost'
CB_BUCKET = CB['BUCKET'] if 'BUCKET' in CB else 'default'
CB_PASSWORD = CB['PASSWORD'] if 'PASSWORD' in CB else CB_BUCKET if CB_BUCKET != 'default' else None


