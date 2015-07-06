"""
utils for couchbase_views
"""


def validate_doctype(doc, type_str):
    """
    validates given couchbase document against type string

    all documents without a matching type or any type attribute at all 
    are considered as invalid

    doc -- instance of `BaseCouchbaseDoc`
    """
    if doc.type:
        return doc.type == type_str
    return False

