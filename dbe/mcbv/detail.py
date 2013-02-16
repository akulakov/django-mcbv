from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db import models
from django.http import Http404
from django.utils.translation import ugettext as _

from base import TemplateResponseMixin, ContextMixin, View


class SingleObjectMixin(ContextMixin):
    """
    Provides the ability to retrieve a single object for further manipulation.
    """
    detail_model               = None
    detail_context_object_name = None
    detail_queryset            = None
    detail_pk_url_kwarg        = 'dpk'
    slug_field                 = 'slug'
    slug_url_kwarg             = 'slug'

    def get_object(self, queryset=None, pk_url_kwarg=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(pk_url_kwarg, None)

        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        elif slug is not None:
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # If none of those are defined, it's an error.
        else:
            raise AttributeError("Generic detail view %s must be called with "
                                 "either an object pk or a slug."
                                 % self.__class__.__name__)

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_detail_object(self, queryset=None):
        return self.get_object( queryset or self.get_detail_queryset(), self.detail_pk_url_kwarg )

    def get_queryset(self, model):
        """
        Get the queryset to look an object up against. May not be called if
        `get_object` is overridden.
        """
        if model:
            return model._default_manager.all()
        else:
            raise ImproperlyConfigured("%(cls)s is missing a queryset. Define "
                                       "%(cls)s.detail_model, %(cls)s.detail_queryset, or override "
                                       "%(cls)s.get_detail_queryset()." % {
                                            'cls': self.__class__.__name__
                                    })

    def get_detail_queryset(self):
        if self.detail_queryset:
            return self.detail_queryset._clone()
        else:
            return self.get_queryset(self.detail_model)

    def get_slug_field(self):
        """
        Get the name of a slug field to be used to look up by slug.
        """
        return self.slug_field

    def get_detail_context_object_name(self, obj):
        """
        Get the name to use for the object.
        """
        if self.detail_context_object_name:
            return self.detail_context_object_name
        elif isinstance(obj, models.Model):
            return obj._meta.object_name.lower()
        else:
            return None

    def get_detail_context_data(self, **kwargs):
        """
        Insert the single object into the context dict.
        """
        context = {}
        context_object_name = self.get_detail_context_object_name(self.detail_object)
        if context_object_name:
            context[context_object_name] = self.detail_object
        context.update(kwargs)
        return context

    def detail_absolute_url(self):
        return self.get_detail_object().get_absolute_url()


class BaseDetailView(SingleObjectMixin, View):
    """
    A base view for displaying a single object
    """
    def detail_get(self, request, *args, **kwargs):
        self.detail_object = self.get_detail_object()
        return self.get_detail_context_data(detail_object=self.detail_object)


class SingleObjectTemplateResponseMixin(TemplateResponseMixin):
    template_name_field = None
    template_name_suffix = '_detail'

    def get_template_names(self):
        return self._get_template_names(self.detail_object, self.detail_model)

    def _get_template_names(self, object=None, model=None):
        """
        Return a list of template names to be used for the request. May not be
        called if render_to_response is overridden. Returns the following list:

        * the value of ``template_name`` on the view (if provided)
        * the contents of the ``template_name_field`` field on the
          object instance that the view is operating upon (if available)
        * ``<app_label>/<object_name><template_name_suffix>.html``
        """
        try:
            names = super(SingleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If self.template_name_field is set, grab the value of the field
        # of that name from the object; this is the most specific template
        # name, if given.
        if object and self.template_name_field:
            name = getattr(self.detail_object, self.template_name_field, None)
            if name:
                names.insert(0, name)

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        if isinstance(object, models.Model):
            names.append("%s/%s%s.html" % (
                object._meta.app_label,
                object._meta.object_name.lower(),
                self.template_name_suffix
            ))
        elif model is not None and issubclass(model, models.Model):
            names.append("%s/%s%s.html" % (
                model._meta.app_label,
                model._meta.object_name.lower(),
                self.template_name_suffix
            ))
        return names


class DetailView(SingleObjectTemplateResponseMixin, BaseDetailView):
    """
    Render a "detail" view of an object.

    By default this is a model instance looked up from `self.queryset`, but the
    view will support display of *any* object by overriding `self.get_object()`.
    """
