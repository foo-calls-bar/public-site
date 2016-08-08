from django.test import Client, TestCase, override_settings
from django.conf import settings

class ContactFormTest(TestCase):
    def __init__(self, *args, **kwargs):
        self.client = Client()
        super(ContactFormTest, self).__init__(*args, **kwargs)

    # @override_settings(DATABASES={'default': settings.DATABASES['replica']})
    def test_valid(self):
        response = self.client.post(
            '/landing/contact/',
            {
                'first_name' : 'ryan',
                'last_name'  : 'kaiser',
                'phone'      : '2146641234',
                'email'      : 'foo@bar.com',
                'comment'    : 'hello world',
                'captcha'    : '123',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        print(response.rendered_content)

    def test_invalid(self):
        response = self.client.post(
            '/landing/contact/',
            {
                'first_name' : 'ryan',
                'last_name'  : 'kaiser',
                'phone'      : '2146641234',
                'email'      : 'foo@bar.com',
                'comment'    : 'hello world',
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        print(response.rendered_content)
#
# from bootstrap3.utils import render_tag
# from bootstrap3.forms import render_field
# from bootstrap3.bootstrap import get_renderer, get_form_renderer, get_field_renderer
# from bootstrap3.bootstrap import get_bootstrap_setting
# from bootstrap3.renderers import FieldRenderer, FormRenderer, InlineFieldRenderer
# from bootstrap3.templatetags import bootstrap3 as ttags
# from landing.views import *
#
# data={
#     'first_name' : 'ryan',
#     'last_name'  : 'kaiser',
#     'phone'      : '2146641234',
#     'email'      : 'foo@bar.com',
#     'comment'    : 'hello world',
#     'captcha'    : '123',
# }
# f = ContactForm(data)
# f.is_valid()
# p = f.fields['phone']
# bf = p.get_bound_field(f,p)

# class TestData:
#     request=HttpRequest()
#     request.method='POST'
#     request.POST=test_data.bad
#     form = ContactForm(request.POST)
#     view=ContactFormView.as_view()
#     vc = view.view_class(**{'request':request})
#     response=view(request)
#     vform = vc.get_form()
#     fields = form.fields
#     captcha = fields['captcha']

# Create your tests here.
