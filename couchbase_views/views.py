__author__ = 'simonwoerpel'

"""
Couchbase designs and views
"""


from django.http import Http404
from django.views.generic import TemplateView

from .connection import CONNECTION as C
from .models import BaseCouchbaseDoc


class BaseView(object):
    def __init__(self, name, view_func=None):
        self.name = name
        if not view_func:
            view_func = {"map": "function (doc, meta) {\n  emit(meta.id, null);\n}"}
        self.view_func = view_func

    def __str__(self):
        return self.name

    def __repr__(self):
        return ': '.join([self.__class__.__name__, self.__str__()])

    def as_json(self):
        return {self.name: self.view_func}


class BaseDesign(object):
    def __init__(self, name, views=None):
        self.name = name
        self.views = views or None

    def __str__(self):
        return self.name

    def __repr__(self):
        return ': '.join([self.__class__.__name__, self.__str__()])

    def create(self):
        if not self.views:
            raise NotImplementedError('Design needs at least one view')
        C.design_create(self.name, {
            'views': self.views.as_json()
        })

    def publish(self):
        C.design_publish(self.name)


class BaseDocumentView(TemplateView):
    """
    base view that puts a single couchbase document into the 'object' context variable
    """

    def get_doc(self):
        """
        retrieves the document from couchbase, based by id 
        submitted via GET
        """
        id = self.request.GET.get('id', None)
        
        if not id:
            raise Http404

        try:
            doc = BaseCouchbaseDoc.get(id)
        except:
            raise Http404
        
    def get_context_data(self, *args, **kwargs):
        """
        adds object to the context
        """
        context = super().get_context_data(*args, **kwargs)
        context['objcect'] = self.get_doc()
        return context

