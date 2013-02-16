# Imports {{{
from collections import OrderedDict, Callable
from string import join

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Model, Manager
from django import forms
# }}}

class UserForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(UserForm, self).__init__(*args, **kwargs)

class UserModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(UserModelForm, self).__init__(*args, **kwargs)

class FormsetModelForm(UserModelForm):
    def __iter__(self):
        """Workaround for a bug in modelformset factory."""
        for name in self.fields:
            if name!="id": yield self[name]

class ContainerFormMixin(object):
    """Wrap form data in a container."""
    def clean(self):
        return Container(**self.cleaned_data)


class BasicModel(Model):
    class Meta: abstract = True
    obj = objects = Manager()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()

BaseModel = BasicModel      # TODO: rename all views to BaseModel

class BaseError(Exception):
    def __init__(self, e): self.e = e
    def __str__(self): return self.e


class Container:
    def __init__(self, **kwds)  : self.__dict__.update(kwds)
    def __setitem__(self, k, v) : self.__dict__[k] = v
    def __delitem__(self, k)    : del self.__dict__[k]
    def __iter__(self)          : return iter(self.__dict__)
    def __getitem__(self, k)    : return self.__dict__[k]
    def __str__(self)           : return str(self.__dict__)
    def __repr__(self)          : return u"Container: <%s>" % repr(self.__dict__)
    def __unicode__(self)       : return unicode(self.__dict__)
    def __nonzero__(self)       : return len(self.__dict__)
    def pop(self, *args)        : return self.__dict__.pop(*args)
    def get(self, *args)        : return self.__dict__.get(*args)
    def update(self, arg)       : return self.__dict__.update(arg)
    def items(self)             : return self.__dict__.items()
    def keys(self)              : return self.__dict__.keys()
    def values(self)            : return self.__dict__.values()
    def dict(self)              : return self.__dict__
    def pp(self)                : pprint(self.__dict__)


class DefaultOrderedDict(OrderedDict):
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
            not isinstance(default_factory, Callable)):
            raise TypeError('first argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy__(self, memo):
        import copy
        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return 'DefaultOrderedDict(%s, %s)' % (self.default_factory, OrderedDict.__repr__(self))


def redir(to, *args, **kwargs):
    if not (to.startswith('/') or to.startswith("http://") or to.startswith("../") or to=='#'):
        to = reverse(to, args=args, kwargs=kwargs)
    return HttpResponseRedirect(to)

def reverse2(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)

def add_csrf(request, **kwargs):
    """Add CSRF to dictionary and wrap in a RequestContext (needed for context processor!)."""
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return RequestContext(request, d)

def render(request, tpl, **kwargs):
    return render_to_response(tpl, add_csrf(request, **kwargs))

def make_paginator(request, items, per_page=50):
    """Make paginator."""
    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    paginator = Paginator(items, per_page)
    try:
        items = paginator.page(page)
    except (InvalidPage, EmptyPage):
        items = paginator.page(paginator.num_pages)
    return items

def updated(dict1, dict2):
    return dict(dict1, **dict2)

def referer(request):
    return request.META["HTTP_REFERER"]

def defdict_to_dict(defdict, constructor=dict):
    """ Recursively convert default dicts to regular dicts.
        constructor: convert to a custom type of dict, e.g. OrderedDict
    """
    if isinstance(defdict, dict):
        new = constructor()
        for key, value in defdict.items():
            new[key] = defdict_to_dict(value, constructor)
        return new
    else:
        return defdict

def defdict_to_odict(defdict):
    from collections import OrderedDict
    return defdict_to_dict(defdict, OrderedDict)

def cjoin(lst):
    return join(lst, ", ")

def float_or_none(val):
    return float(val) if val not in ('', None) else None

def int_or_none(val):
    return int(val) if val not in ('', None) else None

def getitem(iterable, index, default=None):
    """Get item from an `iterable` at `index`, return default if index out of range."""
    try               : return iterable[index]
    except IndexError : return default

def first(iterable, default=None):
    try:
        return next(iter(iterable))
    except StopIteration:
        return default
