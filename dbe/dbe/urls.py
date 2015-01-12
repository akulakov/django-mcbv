from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dbe.views.home', name='home'),

    url(r'^issues/', include('issues.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^bombquiz/', include('bombquiz.urls')),
    url(r'^forum/', include('forum.urls')),
    url(r'^portfolio/', include('portfolio.urls')),
    url(r'^questionnaire/', include('questionnaire.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
