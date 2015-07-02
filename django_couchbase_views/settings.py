__author__ = 'simonwoerpel'

"""
Couchbase Settings
"""


from django.conf import settings

CONNECTION_STR = 'couchbase://localhost/%s' % settings.COUCHBASE_BUCKET
ENTRIES_PER_PAGE = 30
