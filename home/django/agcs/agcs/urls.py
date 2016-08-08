from __future__ import unicode_literals
from django.conf.urls import patterns, url, include
from django.contrib import admin, admindocs
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.shortcuts import urlresolvers

from landing.views import manifest_view
from landing.urls import urlpatterns as landing_urlpatterns
from .sitemaps import StaticViewSitemap

from landing.views import (
    ContactView, HomeView,
    AboutView, ServicesView
)

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [

    url(r'^services/$',
        ServicesView.as_view(),
        name='services'
    ),

    url(r'^about/$',
        AboutView.as_view(),
        name='about'
    ),

    url(r'^contact/$',
        ContactView.as_view(),
        name='contact'
    ),

    url(r'^home/$',
        HomeView.as_view(),
        name='home'
    ),

    url(r'^$',
        HomeView.as_view(),
        name='home'
    ),

    url(r'^manifest\.json$',
        manifest_view,
        name='android_manifest'
    ),

    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url=staticfiles_storage.url('assets/img/favicon/favicon.ico'),
            permanent=False
        ),
        name='favicon'
    ),

    url(r'^admin/doc/',
        include('django.contrib.admindocs.urls')
    ),

    url(r'^admin/',
        admin.site.urls
    ),
]
