import re
import os
from django.conf import settings
from django.template import Library
from django.template.defaulttags import SpacelessNode
from django.template.defaultfilters import stringfilter
from django.template.base import token_kwargs
from django.utils.html import mark_safe, html_safe, format_html, escapejs, escape, force_text,strip_spaces_between_tags
from django.contrib.staticfiles import finders
from css_html_js_minify.minify import prepare
from css_html_js_minify import (
    html_minify, js_minify, css_minify,
)

register = Library()


@html_safe
class InlineResource(object):
    def __init__(self, ftype, path, *paths, **kwargs):
        assert ftype in ['css', 'js']
        self._type = ftype
        self._text = str()
        src_files = list()

        for p in list(finders.find(p) for p in (path,) + paths):
            if not os.path.isdir(p):
                src_files.append(p)
                continue

            src_files.extend(
                os.path.join(p, s) for s in os.listdir(p)
                    if os.path.isfile(os.path.join(p, s))
                        and s.endswith(self._type)
            )

        for src in src_files:
            with open(src, encoding="utf-8") as s:
                self._text += "\n" + s.read()

        self.mini = kwargs.get('mini', getattr(settings, 'MINIFY_INLINE_RESOURCS', True))

    @property
    def text(self):
        return self._text

    @property
    def minified(self):
        return (self._type is 'js'
            and js_minify(self._text)
            or  css_minify(self._text)
        )

    def __str__(self):
        return self.mini and self.minified or self.text


@register.simple_tag
def inline_js_file(path, *paths, **kwargs):
    return mark_safe(str(InlineResource('js', path, *paths, **kwargs)))

@register.simple_tag
def inline_css_file(path, *paths, **kwargs):
    return mark_safe(str(InlineResource('css', path, *paths, **kwargs)))

@register.simple_tag
def async_css(href):
    return format_html(''.join([
        '<link rel="preload" href="{0}" as="style" onload="this.rel=\'stylesheet\'">',
        '<noscript><link rel="stylesheet" href="{0}"></noscript>'
    ]), href)

@register.filter
@stringfilter
def minify_js(value):
    return mark_safe(js_minify(value))

@register.filter
@stringfilter
def minify_css(value):
    return mark_safe(css_minify(value))

@register.filter
@stringfilter
def minify_html(value):
    return mark_safe(html_minify(value))

def _append(value, arg):
    return value + arg

@register.assignment_tag
@register.filter
def append(value, arg):
    return _append(value, arg)

@register.assignment_tag
@register.filter
def append(value, arg):
    return _append(value, arg)

@register.filter
def listsort(value):
    return sorted(value)

@register.filter
def listsortreversed(value):
    return sorted(value, reverse=True)

@register.filter
@stringfilter
def split(value, char=','):
    return value.split(char)

mklist = split

@register.filter
@stringfilter
def mkattribute(value):
    return re.sub(" ?[&/\\@ ] ?", '_', value)[0:20]

@register.filter
@stringfilter
def find(value, substr):
    return value.find(substr)
