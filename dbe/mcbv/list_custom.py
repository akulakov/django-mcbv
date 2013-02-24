from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse

from list import *
from edit_custom import *


class PaginatedSearch(ListView, SearchFormView):
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
    object_list = None

    def get_list_queryset(self):
        return self.object_list or []

    def get_list_context_data(self, **kwargs):
        context = super(PaginatedSearch, self).get_list_context_data(**kwargs)
        get     = self.request.GET.copy()
        get.pop("page", None)
        extra = '&'+get.urlencode()
        return dict(context, extra_vars=extra, form=self.get_form())


class ListFilterView(PaginatedSearch):
    """Filter a list view through a search."""
    list_model   = None
    search_field = 'q'
    start_blank  = True     # start with full item listing or blank page

    def get_list_queryset(self):
        if self.object_list:
            return self.object_list
        else:
            return list() if self.start_blank else self.list_model.objects.all()

    def get_query(self, q):
        return Q()

    def form_valid(self, form):
        q                = form.cleaned_data[self.search_field].strip()
        filter           = self.list_model.objects.filter
        self.object_list = filter(self.get_query(q)) if q else None
        return dict(form=form)


class ListRelated(DetailView, ListView):
    """Listing of an object and related items."""
    related_name = None      # attribute name linking main object to related objects

    def get_list_queryset(self):
        obj = self.get_detail_object()
        return getattr(obj, self.related_name).all()


class DetailListCreateView(ListRelated, CreateView):
    """ DetailView of an object & listing of related objects and a form to create new related obj.

        fk_attr : field of object to be created that points back to detail_object, e.g.:
                    detail_model = Thread; fk_attr = "thread"; reply.thread = detail_object
    """
    success_url = '#'
    fk_attr     = None

    def modelform_valid(self, modelform):
        self.modelform_object = modelform.save(commit=False)
        setattr(self.modelform_object, self.fk_attr, self.get_detail_object())
        self.modelform_object.save()
        return HttpResponseRedirect(self.get_success_url())


class DetailListFormSetView(ListRelated, ModelFormSetView):
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
    main_object                = None  # should be left as None in subclass
    extra                      = 0
    template_name              = None

    def get_formset_queryset(self):
        qset      = self.get_list_queryset()
        page_size = self.get_paginate_by(qset)
        if page_size : return self.paginate_queryset(qset, page_size)[2]
        else         : return qset


class PaginatedModelFormSetView(ListView, ModelFormSetView):
    detail_model               = None
    list_model                 = None
    formset_model              = None
    related_name               = None
    detail_context_object_name = None
    formset_form_class         = None
    paginate_by                = None
    main_object                = None  # should be left as None in subclass
    extra                      = 0
    template_name              = None

    def get_formset_queryset(self):
        # qset      = super(PaginatedModelFormSetView, self).get_formset_queryset()
        qset      = self.get_list_queryset()
        page_size = self.get_paginate_by(qset)
        if page_size : return self.paginate_queryset(qset, page_size)[2]
        else         : return qset
