from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from django.shortcuts import urlresolvers
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_page

from .views import (
    ContactView, HomeView,
    AboutView, ServicesView
)

app_name = 'landing'

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
]

class URLset(object):
    patterns = urlpatterns

    @staticmethod
    def root_url_patterns():
        return [
            url(r'' + pattern.regex.pattern,
                RedirectView.as_view(
                    url=urlresolvers.reverse('landing:' + pattern.name),
                    permanent=False
                ),
                name=pattern.name
            ) for pattern in URLset.patterns
        ]

    @staticmethod
    def root_url(name):
        try:
            return [p for p in URLset.root_url_patterns() if p.name is name][0]
        except IndexError:
            return None
