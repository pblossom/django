import os

from django import forms
from django.template.backends.django import DjangoTemplates
from django.template.loader import get_template
from django.utils._os import upath
from django.utils.functional import cached_property

ROOT = upath(os.path.dirname(forms.__file__))


class BaseTemplateRenderer(object):
    def get_template(self, template_name):
        raise NotImplementedError('subclasses must implement get_template()')

    def render(self, template_name, context, request=None):
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()


class EngineRendererMixin(object):
    def get_template(self, template_name):
        return self.engine.get_template(template_name)


class DjangoTemplateRenderer(EngineRendererMixin, BaseTemplateRenderer):
    """
    Load Django templates from app directories and the built-in widget
    templates in django/forms/templates.
    """
    @cached_property
    def engine(self):
        return DjangoTemplates({
            'APP_DIRS': True,
            'DIRS': [os.path.join(ROOT, 'templates')],
            'NAME': 'djangoforms',
            'OPTIONS': {},
        })


class Jinja2TemplateRenderer(EngineRendererMixin, BaseTemplateRenderer):
    """
    Load Jinja2 templates from app directories and the built-in widget
    templates in django/forms/jinja2.
    """
    @cached_property
    def engine(self):
        from django.template.backends.jinja2 import Jinja2
        return Jinja2({
            'APP_DIRS': True,
            'DIRS': [os.path.join(ROOT, 'jinja2')],
            'NAME': 'djangoforms',
            'OPTIONS': {},
        })


class ProjectTemplateRenderer(BaseTemplateRenderer):
    def get_template(self, template_name):
        return get_template(template_name)
