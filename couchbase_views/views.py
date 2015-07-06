__author__ = 'simonwoerpel'

"""
Couchbase designs and views
"""


from django.http import Http404
from django.views.generic import TemplateView

from .connection import CONNECTION as C
from .models import BaseCouchbaseDoc
from .utils import validate_doctype


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

    set `doc_type` to limit doc retrieving for this type (couchbase documents must have therefore
    a 'type' attribute)
    this attribute will also affect `get_template_names`
    """
    doc_type = None
    template_name = 'couchbase_views/document_detail.html'

    def get_doc_type(self):
        return self.doc_type

    def get_doc(self):
        """
        retrieves the document from couchbase, based by id 
        """
        id = self.kwargs.pop('id', None)
        
        if not id:
            raise Http404

        try:
            doc = BaseCouchbaseDoc.get(id)
        except:
            raise Http404

        if self.doc_type and not validate_doctype(doc, self.get_doc_type()):
            raise Http404

        return doc
        
    def get_context_data(self, *args, **kwargs):
        """
        adds object to the context
        """
        context = super().get_context_data(*args, **kwargs)
        context['object'] = self.get_doc()
        return context

    def get_template_names(self, *args, **kwargs):
        if self.get_doc_type():
            return ['%s_detail.html' % self.get_doc_type()] + super().get_template_names(*args, **kwargs)
        return super().get_template_names(*args, **kwargs)

