from django import template
from django.conf import settings

from dbe.shared.utils import cjoin

register = template.Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

def get(value, arg):
    return value[arg]

def list_related(value):
    if hasattr(value, "all"):
        return cjoin(str(i) for i in value.all())
    return value

def concat(value, arg):
    return value + arg


register.filter("getattribute", getattribute)
register.filter("get", get)
register.filter("concat", concat)
register.filter("list_related", list_related)
