import re
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import (
    format_html_join,
    format_html,
    urlize as _urlize
)
from .models import Contact, STATUS_CHOICES

# admin.site.disable_action('delete_selected')

phone_number_re = re.compile(
    '^(\+?\d-?)?(\d{3}-?){2}\d{4}$',
    flags=re.IGNORECASE+re.UNICODE
)

def urlize(text, target='_blank', *args, **kwargs):
    def add_target(text):
        return text.replace('href=', 'target="_blank" href=')
    def do_phone():
        return format_html(
            mark_safe('<a target="{1}" href="tel:{0}">{0}</a>'),
            text, target
        )
    return mark_safe(
        add_target(phone_number_re.match(text)
            and do_phone() or _urlize(text, *args, **kwargs)
        )
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_filter     = ('status', 'date',)
    list_display    = ('date', 'status', 'name', 'email', 'phone', 'comment',)
    actions         = ['mark_closed', 'mark_responded', 'mark_new', 'delete_selected']
    ordering        = ['date', 'status',]
    date_hierarchy  = 'date'
    fields          = (
        'status', 'notes',
        'name', 'date',
        'email_report', 'phone_report',
        'comment_report',
        'remote_address'
    )

    readonly_fields = fields[2:]

    def email_report(self, instance):
        return urlize(
            instance.email
        ) or mark_safe("<span class='errors'>I can't determine this email.</span>")

    def phone_report(self, instance):
        return urlize(
            instance.phone
        ) or mark_safe("<span class='errors'>I can't determine this number.</span>")

    def comment_report(self, instance):
        return format_html(
            mark_safe('<span style="font-size: large;"><b>{}</b></span>'),
            instance.comment
        ) or mark_safe("<span class='errors'>I can't determine this comment.</span>")

    def change_status(self, status, request, queryset):
        choices = [x[0] for x in STATUS_CHOICES]
        if choices.count(status):
            rows_updated = queryset.update(status=status)
            if rows_updated == 1:
                message_bit = "1 isssue was"
            else:
                message_bit = "{0} issue were".format(rows_updated)
            self.message_user(request, "{0} successfully marked {1}.".format(
                message_bit, STATUS_CHOICES[choices.index(status)][1]
            ))

    def mark_closed(self, *args):
        self.change_status('c', *args)

    def mark_responded(self, *args):
        self.change_status('r', *args)

    def mark_new(self, *args):
        self.change_status('n', *args)

    phone_report.short_description   = "Phone"
    email_report.short_description   = "Email"
    comment_report.short_description = "Comment"
    mark_closed.short_description    = 'Mark selected issues as closed'
    mark_responded.short_description = "Mark selected issues as responded to"
    mark_new.short_description       = "Mark selected issues as new"
