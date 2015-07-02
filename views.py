__author__ = 'simonwoerpel'

"""
Couchbase designs and views
"""


from .connection import CONNECTION as C


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

