"""
urls for couchbase_views
"""

from django.conf.urls import include, url

from .views import BaseDocumentView


urlpatterns = [
    url(r'^(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$', 
        BaseDocumentView.as_view(),
        name='cb-document-detail',
    )
]
