# -*- coding: utf-8 -*-
"""
Jinja2 templates for deform.

To use in Pyramid:

In your settings.ini::

    # default:
    # deform_jinja2.i18n.domain=deform

    # One of:
    deform_jinja2.template_search_path=deform_jinja2:templates
    deform_jinja2.template_search_path=deform_jinja2:uni_templates
    deform_jinja2.template_search_path=deform_jinja2:bootstrap_templates

In your app initialization::

    config.include('deform_jinja2')

"""

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2.utils import import_string
from pkg_resources import resource_filename

from compat import string_types


def splitlines(s):
    return filter(None, [x.strip() for x in s.splitlines()])


def maybe_import_string(val):
    if isinstance(val, string_types):
        return import_string(val.strip())
    return val


def parse_config(config):
    """
    Parses config values from .ini file and returns a dictionary with
    imported objects
    """
    # input must be a string or dict
    result = {}
    if isinstance(config, string_types):
        for f in splitlines(config):
            name, impl = f.split('=', 1)
            result[name.strip()] = maybe_import_string(impl)
    else:
        for name, impl in config.items():
            result[name] = maybe_import_string(impl)
    return result


class DummyTranslator(object):
    @staticmethod
    def gettext(message):
        return message

    @staticmethod
    def ngettext(singular, plural, n):
        if n > 1:
            return plural

        return singular


class jinja2_renderer_factory(object):
    def __init__(self, search_paths=(),
                 default_templates='deform_jinja2:templates',
                 translator=None, extensions=[], filters=None):

        if 'jinja2.ext.i18n' not in extensions:
            extensions.append('jinja2.ext.i18n')

        self.env = Environment(extensions=extensions)
        self.env.loader = FileSystemLoader(())

        for path in search_paths:
            self.add_search_path(path)

        if translator is None:
            translator = DummyTranslator

        self.env.install_gettext_callables(translator.gettext,
                                           translator.ngettext)

        self.add_search_path(default_templates)

        filters = filters or {}
        self.env.filters.update(filters)

    def add_search_path(self, path):
        self.env.loader.searchpath.append(
            resource_filename(*(path.split(':'))))

    def __call__(self, tname, **kw):
        if not '.jinja2' in tname:
            tname += '.jinja2'

        template = self.env.get_template(tname)
        return template.render(**kw)


def includeme(config):
    from translator import PyramidTranslator
    import deform
    settings = config.registry.settings
    domain = settings.get('deform_jinja2.i18n.domain', 'deform')
    search_path = settings.get('deform_jinja2.template_search_path', '')
    filters = parse_config(settings.get('deform_jinja2.filters', ''))

    renderer = jinja2_renderer_factory(
        search_paths=search_path.strip().split(),
        translator=PyramidTranslator(domain=domain),
        filters=filters
    )
    deform.Form.set_default_renderer(renderer)
