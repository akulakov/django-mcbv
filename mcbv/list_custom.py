from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse

from list import *
from edit_custom import *


class ListFilterView(ListView, SearchFormViewMixin):
    """ List Filter - filter list with a search form.

        as_view      : dispatch -> get or post
        get          : get_form OR get_queryset -> get_context_data -> render_to_response
        post         : get_form -> get_form_kwargs -> form_valid or form_invalid
        form_valid   : get_success_url
        form_invalid : get_context_data -> render_to_response

        as_view, dispatch      : base.View
        render_to_response     : TemplateResponseMixin

        get                    : BaseListView
        post                   : ProcessFormView
        get_form, form_invalid : FormMixin
        get_form_kwargs        : SearchFormViewMixin

        form_valid, get_success_url, get_queryset, get_context_data
    """
    context_object_name = None
    success_url_name    = None
    q                   = Q()

    def get(self, request):
        self.object_list = self.model.obj.all()
        form             = self.get_form()
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def get_success_url(self):
        return reverse(self.success_url_name) if self.success_url_name else None

    def get_queryset(self):
        return self.model.objects.filter(self.q)

    def form_valid(self, form):
        u = self.get_success_url()
        if u: return HttpResponseRedirect(u)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        # search query to be added to page links
        get = self.request.GET.copy()
        get.pop("page", None)
        kwargs.update({"object_list"            : self.object_list,
                       "extra_vars"             : '&'+get.urlencode(),
                       self.context_object_name : self.object_list,
                       })
        c = super(ListFilterView, self).get_context_data(**kwargs)
        c.update( dict(form=self.get_form()) )
        return c


class ListRelated(DetailView, ListView):
    """Listing of an object and related items."""
    related_name = None      # attribute name linking main object to related objects

    def get_list_queryset(self):
        obj = self.get_detail_object()
        return getattr(obj, self.related_name).all()


class DetailListCreateView(ListRelated, CreateView):
    """DetailView of an object & listing of related objects and a form to create new related obj."""
    success_url = '#'
    fk_attr     = None  # modelform_obj.`fk_attr` -> detail_object

    def form_valid(self, form, modelform, _):
        resp = super(DetailListCreateView, self).form_valid(_, modelform, _)
        setattr(self.modelform_object, self.fk_attr, self.get_detail_object())
        return resp


class DetailListFormsetView(ListRelated, FormSetView):
    """ List of items related to main item, viewed as a paginated formset.
        Note: `list_model` needs to have ordering specified for it to be able to paginate.
    """
    detail_model               = None
    list_model                 = None
    formset_model              = None
    related_name               = None
    detail_context_object_name = None
    formset_form_class         = None
    paginate_by                = None
    template_name              = None
    main_object                = None  # should be left as None in subclass

    def get_formset(self, form_class=None):
        Formset   = modelformset_factory(self.formset_model, form=self.formset_form_class, extra=0)
        qs        = self.get_list_queryset()
        page_size = self.get_paginate_by(qs)
        request   = self.request
        if page_size:
            qs = self.paginate_queryset(qs, page_size)[2]

        if request.method=="POST" : return Formset(request.POST, queryset=qs)
        else                      : return Formset(queryset=qs)
