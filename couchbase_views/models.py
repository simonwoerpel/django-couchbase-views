__author__ = 'simonwoerpel'

"""
Couchbase Docs as Python objects inspired from django.models
"""


import uuid

from .connection import CONNECTION as C
# from .views import BaseDesign, BaseView


class BaseCouchbaseDoc(object):
    """
    the base class for all
    """
    def __init__(self, doc):
        self.doc = doc
        self.key = self.doc.key

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.doc.value.get(name, None)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self._update_doc()

    def _update_doc(self):
        for k, v in self.__dict__.items():
            if k not in ('key', 'doc'):
                self.doc.value[k] = str(v)

    def save(self):
        self._update_doc()
        C.upsert(self.key, self.doc.value)

    def delete(self):
        C.remove(self.key)

    @classmethod
    def get(cls, key):
        """
        retrieves document by given key from couchbase connection
        and returns a BaseCouchbaseDoc instance for the retrieved doc
        """
        doc = C.get(key)
        return cls(doc)

    @classmethod
    def get_multi(cls, keys):
        """
        'keys' must be an iterable
        """
        docs = C.get_multi(keys)
        return [cls(docs[key]) for key in docs]

    @classmethod
    def create(cls, data):
        """
        creates a new document from couchbase connection
        :param data: dict
        :return: BaseCouchbaseDoc instance with the newly created doc
        """
        key = str(uuid.uuid4())
        C.insert(key, data)
        return cls.get(key)


class BaseCouchbaseModel(BaseCouchbaseDoc):

    def __init__(self, doc):
        super().__init__(doc)
        if not self.type:
            self.type = self.__class__.__name__.lower()
            self.save()

    def __repr__(self):
        return ': '.join([self.__class__.__name__, self.__str__()])

    @classmethod
    def _design_name(cls):
        return cls.__name__.lower()

    # @classmethod
    # def _design(cls):
    #     return BaseDesign(cls._design_name())

    # @classmethod
    # def _base_view(cls):
    #     view_func = {"map": "function (doc, meta) {\nif (doc.type == '%s') {\n    emit(meta.id, null);\n}}"
    #                         % cls.__name__.lower()}
    #     return BaseView('all', view_func)

    @classmethod
    def all(cls):
        return [i for i in C.query(cls._design_name(), 'all').__iter__()]

    @classmethod
    def get_all(cls):
        return cls.get_multi([i.docid for i in cls.all()])

