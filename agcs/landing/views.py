from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.conf import settings
from django.views.generic.base import RedirectView
from django.utils.decorators import method_decorator

from .models import Contact
from .forms import ContactForm
from .mixins import CacheMixin, NeverCacheMixin

class AutoTitleView(object):
    page_title = None

    @property
    def title(self):
        return (self.page_title and
            self.page_title or
            self.template_name
                .rpartition('/')[-1]
                .rpartition('.')[0]
                .replace('_', ' ')
        )

    @title.setter
    def title(self, title):
        self.page_title = title

    @property
    def common_context(self):
        return {
            self.title : True,
            'pages'    : getattr(self, 'pages', []),
            'title'    : getattr(self, 'title', None),
            'DEBUG'    : getattr(settings, 'DEBUG', False),
            'company'  : getattr(settings, 'COMPANY', None),
            'gapi_key' : getattr(settings, 'GOOGLE_API_KEY', None),
        }


class LandingPageView(CacheMixin, TemplateView, AutoTitleView):
    cache_timeout = settings.DEBUG and 5 or 3600
    pages = ['home', 'services', 'about', 'contact']

    def get_context_data(self, **kwargs):
        context = super(LandingPageView, self).get_context_data(**kwargs)
        context.update(self.common_context)
        return context


class HomeView(LandingPageView):
    template_name = 'landing/pages/home.html'


class AboutView(LandingPageView):
    template_name = 'landing/pages/about.html'


class ServicesView(LandingPageView):
    template_name = 'landing/pages/services.html'
    services = [
        'Backup Solutions','Custom Builds', 'Lessons',
        'Mobile Devices','Networking','VPN Solutions',
        'Planning/Consulting','New Device Setup',
        'Viruses/Spyware','Maintenance','Repairs',
    ]

    def get_context_data(self, **kwargs):
        context = super(ServicesView, self).get_context_data(**kwargs)
        context.update({'services': self.services})
        return context


class ContactView(FormView, AutoTitleView):
    pages = LandingPageView.pages
    template_name = 'landing/pages/contact.html'
    success_url = '/contact/'
    form_class = ContactForm
    send_email = True

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context.update(self.common_context)
        return context

    def form_valid(self, form):
        form.instance.remote_address = self.request.META.get('HTTP_X_REAL_IP', '0.0.0.0')
        self.object = form.save()
        self.send_email and form.send_email()
        messages.success(self.request,
            'Thanks! Someone will contact you soon.',
            extra_tags='form_valid',
        )
        return super(ContactView, self).form_valid(form)


@cache_page(settings.DEBUG and 5 or 86400)
def manifest_view(request):
    return JsonResponse({
        'name': 'AGCS',
        'display': 'standalone',
        'icons': settings.ANDROID_ICONS
    }, json_dumps_params={'indent': 2})
