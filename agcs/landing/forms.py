import random
from collections import OrderedDict, namedtuple
from string import ascii_letters as _letters
from string import digits as _digits
from django import forms
from django.forms import fields_for_model
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives, BadHeaderError
from django.views.decorators.http import require_POST
from django.core import validators
from django.template.loader import render_to_string
from collections import namedtuple, OrderedDict
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget
from .models import *


def random_int(len=1, choices=_digits):
    return int(''.join(random.choice(str(choices)) for i in range(len)))


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'phone', 'email', 'comment']

    cc_myself = forms.BooleanField(required=False, initial=False)
    captcha = ReCaptchaField(label="   ", widget=ReCaptchaWidget())

    def send_email(self):

        try:
            msg = EmailMultiAlternatives(
                subject='Contact Form: ' + str(self.instance.name),
                from_email=settings.EMAIL_HOST_USER,
                reply_to=[self.cleaned_data['email']],
                to=tuple(i[1] for i in settings.ADMINS) + (
                    self.cleaned_data['cc_myself'] and
                    (self.cleaned_data['email'],) or tuple()
                ),
                body=''.join(
                    '{0:15s} : {1}\n'.format(
                        self.fields[f].label, self.cleaned_data[f]
                    ) for f in self._meta.fields
                )
            )

            msg.attach_alternative(
                render_to_string(
                    'landing/email/contact_form.html',
                    context={
                        'name'    : str(self.instance.name),
                        'phone'   : self.cleaned_data['phone'],
                        'email'   : self.cleaned_data['email'],
                        'comment' : self.cleaned_data['comment'],
                    }
                ), "text/html"
            )

            msg.send()

        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        except Exception as e:
            print(e)
            return False
        return True
