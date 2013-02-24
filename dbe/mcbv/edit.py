from django.forms import models as model_forms
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.db import models
from django.contrib import messages

from django.utils.functional import curry
from django.forms.formsets import formset_factory, BaseFormSet, all_valid
from django.forms.models import modelformset_factory

from base import TemplateResponseMixin, ContextMixin, View
from detail import SingleObjectMixin, SingleObjectTemplateResponseMixin, BaseDetailView, DetailView
from list import MultipleObjectMixin, ListView


class FormMixin(ContextMixin):
    """
    A mixin that provides a way to show and handle a form in a request.
    """

    initial         = {}
    form_class      = None
    success_url     = None
    form_kwarg_user = False     # provide request user to form

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """
        return self.initial.copy()

    def get_form_class(self):
        """
        Returns the form class to use in this view
        """
        return self.form_class

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        form_class = form_class or self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {'initial': self.get_initial()}
        if self.form_kwarg_user:
            kwargs['user'] = self.request.user

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        """
        Returns the supplied success URL.
        """
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """
        If the form or modelform are invalid, re-render the context data with the
        data-filled form and errors.
        """
        return self.get_context_data(form=form)


class FormSetMixin(FormMixin):
    """A mixin that provides a way to show and handle a formset in a request."""
    formset_form_class = None
    formset_initial    = {}
    formset_class      = BaseFormSet
    extra              = 0
    can_delete         = False
    # ignore_get_args    = ("page", )     # TODO this may be better moved to the form class?

    formset_kwarg_user = False       # provide request user to form
    success_url        = None

    def get_formset_initial(self):
        return self.formset_initial.copy()

    def get_formset_class(self):
        return self.formset_class

    def get_formset_form_class(self):
        return self.formset_form_class

    def get_formset(self, form_class=None):
        form_class = form_class or self.formset_form_class
        kwargs     = dict()
        Formset    = formset_factory(form_class, extra=self.extra, can_delete=self.can_delete)

        if self.form_kwarg_user:
            kwargs["user"] = self.user

        Formset.form = staticmethod(curry(form_class, **kwargs))
        return Formset(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = dict(initial=self.get_formset_initial())

        if self.formset_kwarg_user:
            kwargs["user"] = self.request.user

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_success_url(self):
        if self.success_url:
            # Forcing possible reverse_lazy evaluation
            url = force_text(self.success_url)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")
        return url

    def formset_valid(self, formset):
        for form in formset:
            if form.has_changed():
                if form.cleaned_data.get("DELETE"):
                    self.process_delete(form)
                else:
                    self.process_form(form)
        return HttpResponseRedirect(self.get_success_url())

    def process_form(self, form):
        form.save()

    def process_delete(self, form):
        """Process checked 'delete' box."""
        pass

    def formset_invalid(self, formset):
        return self.get_context_data(formset=formset)


class ModelFormSetMixin(FormSetMixin):
    formset_model    = None
    formset_queryset = None

    def get_formset_queryset(self):
        if self.formset_queryset is not None:
            queryset = self.formset_queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.formset_model is not None:
            queryset = self.formset_model._default_manager.all()
        else:
            raise ImproperlyConfigured("'%s' must define 'formset_queryset' or 'formset_model'"
                                        % self.__class__.__name__)
        return queryset

    def get_formset(self, form_class=None):
        form_class = form_class or self.formset_form_class
        kwargs     = dict()
        Formset    = modelformset_factory(self.formset_model, extra=self.extra, can_delete=self.can_delete)

        if self.form_kwarg_user:
            kwargs["user"] = self.user

        Formset.form = staticmethod(curry(form_class, **kwargs))
        return Formset(**self.get_formset_kwargs())

    def get_formset_kwargs(self):
        kwargs = {
                  'initial'  : self.get_formset_initial(),
                  'queryset' : self.get_formset_queryset(),
                  }

        if self.formset_kwarg_user:
            kwargs["user"] = self.request.user

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def process_delete(self, form):
        """Process checked 'delete' box."""
        form.instance.delete()


class ModelFormMixin(FormMixin, SingleObjectMixin):
    """
    A mixin that provides a way to show and handle a modelform in a request.
    """
    form_model                    = None
    modelform_class               = None
    modelform_queryset            = None
    modelform_context_object_name = None
    modelform_pk_url_kwarg        = 'mfpk'
    modelform_valid_msg           = None

    def get_modelform_class(self):
        """Returns the form class to use in this view."""
        if self.modelform_class:
            return self.modelform_class
        else:
            if self.form_model is not None:
                # If a model has been explicitly provided, use it
                model = self.form_model
            elif hasattr(self, 'modelform_object') and self.modelform_object is not None:
                # If this view is operating on a single object, use
                # the class of that object
                model = self.modelform_object.__class__
            else:
                # Try to get a queryset and extract the model class
                # from that
                model = self.get_modelform_queryset().model
            return model_forms.modelform_factory(model)

    def get_modelform(self, form_class=None):
        form_class = form_class or self.get_modelform_class()
        return form_class(**self.get_modelform_kwargs())

    def get_modelform_kwargs(self):
        """Returns the keyword arguments for instantiating the form."""
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.modelform_object})
        return kwargs

    def get_success_url(self):
        """Returns the supplied URL."""
        if self.success_url:
            url = self.success_url % self.modelform_object.__dict__
        else:
            try:
                url = self.modelform_object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url

    def modelform_valid(self, modelform):
        self.modelform_object = modelform.save()
        if self.modelform_valid_msg:
            messages.info(self.request, self.modelform_valid_msg)
        return HttpResponseRedirect(self.get_success_url())

    def modelform_invalid(self, modelform):
        return self.get_context_data(modelform=modelform)

    def get_modelform_context_data(self, **kwargs):
        """
        If an object has been supplied, inject it into the context with the
        supplied modelform_context_object_name name.
        """
        context = {}
        obj = self.modelform_object
        if obj:
            context['modelform_object'] = obj
            if self.modelform_context_object_name:
                context[self.modelform_context_object_name] = obj
            elif isinstance(obj, models.Model):
                context[obj._meta.object_name.lower()] = obj
        context.update(kwargs)
        return context

    def get_modelform_object(self, queryset=None):
        return self.get_object( queryset or self.get_modelform_queryset(), self.modelform_pk_url_kwarg )

    def get_modelform_queryset(self):
        if self.modelform_queryset:
            return self.modelform_queryset._clone()
        else:
            return self.get_queryset(self.form_model)


class ProcessFormView(View):
    """
    A mixin that renders a form on GET and processes it on POST.
    """

    def form_get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        return self.get_context_data( form=self.get_form() )

    def formset_get(self, request, *args, **kwargs):
        return self.get_context_data( formset=self.get_formset() )

    def modelform_get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates a blank version of the form.
        """
        return self.get_modelform_context_data( modelform=self.get_modelform() )

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = formset = modelform = None

        if isinstance(self, DetailView):
            self.detail_object = self.get_detail_object()

        if isinstance(self, ListView):
            self.object_list = self.get_list_queryset()

        if isinstance(self, FormView):
            form = self.get_form()

        if isinstance(self, (FormSetView, ModelFormSetView)):
            formset = self.get_formset()

        if isinstance(self, UpdateView):
            self.update_post(request, *args, **kwargs)
            modelform = self.get_modelform()

        if isinstance(self, CreateView):
            self.create_post(request, *args, **kwargs)
            modelform = self.get_modelform()

        if (not form or form and form.is_valid()) and \
           (not modelform or modelform and modelform.is_valid()) and \
           (not formset or formset and formset.is_valid()):

            if isinstance(self, FormView)                        : resp = self.form_valid(form)
            if isinstance(self, (FormSetView, ModelFormSetView)) : resp = self.formset_valid(formset)
            if isinstance(self, (UpdateView, CreateView))        : resp = self.modelform_valid(modelform)
            return resp

        else:
            context = self.get_context_data()
            update  = context.update
            if isinstance(self, FormView)                        : update(self.form_invalid(form))
            if isinstance(self, (FormSetView, ModelFormSetView)) : update(self.formset_invalid(formset))
            if isinstance(self, (UpdateView, CreateView))        : update(self.modelform_invalid(modelform))
            return self.render_to_response(context)

    # PUT is a valid HTTP verb for creating (with a known URL) or editing an
    # object, note that browsers only support POST for now.
    def put(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class BaseFormView(FormMixin, ProcessFormView):
    """ A base view for displaying a form """

class FormView(TemplateResponseMixin, BaseFormView):
    """ A view for displaying a form, and rendering a template response. """

class BaseFormSetView(FormSetMixin, ProcessFormView):
    """A base view for displaying a formset."""

class FormSetView(TemplateResponseMixin, BaseFormSetView):
    """A view for displaying a formset, and rendering a template response."""


class BaseModelFormSetView(ModelFormSetMixin, ProcessFormView):
    """A base view for displaying a modelformset."""

class ModelFormSetView(TemplateResponseMixin, BaseModelFormSetView):
    """A view for displaying a modelformset, and rendering a template response."""



class BaseCreateView(ModelFormMixin, ProcessFormView):
    """
    Base view for creating an new object instance.

    Using this base class requires subclassing to provide a response mixin.
    """
    def create_get(self, request, *args, **kwargs):
        self.modelform_object = None
        return self.modelform_get(request, *args, **kwargs)

    def create_post(self, request, *args, **kwargs):
        self.modelform_object = None


class CreateView(SingleObjectTemplateResponseMixin, BaseCreateView):
    """
    View for creating a new object instance,
    with a response rendered by template.
    """
    template_name_suffix = '_modelform'

    def get_template_names(self):
        return self._get_template_names(self.modelform_object, self.form_model)


class BaseUpdateView(ModelFormMixin, ProcessFormView):
    """
    Base view for updating an existing object.

    Using this base class requires subclassing to provide a response mixin.
    """
    def update_get(self, request, *args, **kwargs):
        self.modelform_object = self.get_modelform_object()
        return self.modelform_get(request, *args, **kwargs)

    def update_post(self, request, *args, **kwargs):
        self.modelform_object = self.get_modelform_object()


class UpdateView(SingleObjectTemplateResponseMixin, BaseUpdateView):
    """
    View for updating an object,
    with a response rendered by template.
    """
    template_name_suffix = '_modelform'

    def get_template_names(self):
        return self._get_template_names(self.modelform_object, self.form_model)


class CreateUpdateView(CreateView):
    """Update object if modelform_pk_url_kwarg is in kwargs, otherwise create it."""
    modelform_create_class = None

    def get_modelform_class(self):
        if self.modelform_pk_url_kwarg in self.kwargs:
            return self.modelform_class
        else:
            return self.modelform_create_class

    def create_get(self, request, *args, **kwargs):
        if self.modelform_pk_url_kwarg in self.kwargs:
            self.modelform_object = self.get_modelform_object()
            return self.modelform_get(request, *args, **kwargs)
        else:
            return super(CreateUpdateView, self).create_get(request, *args, **kwargs)

    def create_post(self, request, *args, **kwargs):
        if self.modelform_pk_url_kwarg in self.kwargs:
            self.modelform_object = self.get_modelform_object()
        else:
            super(CreateUpdateView, self).create_post(request, *args, **kwargs)


class DeletionMixin(object):
    """
    A mixin providing the ability to delete objects
    """
    success_url = None

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.modelform_object = self.get_modelform_object()
        self.modelform_object.delete()
        return HttpResponseRedirect(self.get_success_url())

    # Add support for browsers which only accept GET and POST for now.
    def post(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseDeleteView(DeletionMixin, BaseDetailView):
    """
    Base view for deleting an object.

    Using this base class requires subclassing to provide a response mixin.
    """


class DeleteView(SingleObjectTemplateResponseMixin, BaseDeleteView):
    """
    View for deleting an object retrieved with `self.get_object()`,
    with a response rendered by template.
    """
    template_name_suffix = '_confirm_delete'
