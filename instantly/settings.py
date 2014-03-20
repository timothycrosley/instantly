""" instantly/settings.py

Defines how instantly discovers and exposes settings and templates.

Copyright (C) 2013  Timothy Edmund Crosley

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
from glob import glob

from configobj import ConfigObj
from pies.collections import OrderedDict
from pies.functools import lru_cache
from pies.overrides import *

from . import _first_template
from .template import LocalTemplate

MAX_CONFIG_SEARCH_DEPTH = 25 # The number of parent directories instantly will look for a config file within

default = {'auto_update_templates': True,
           'templates': {},
           'path': os.path.expanduser('~/.instant_templates'),
           'defaults': {}}

@lru_cache()
def from_path(path):
    computed_settings = default.copy()
    _update_settings_with_config(path, '.instant_templates', "~/.instant_templates", ('settings', ),
                                 computed_settings)
    return computed_settings


def create(directory):
    first_template = os.path.join(directory, 'create_instant_template')
    os.makedirs(first_template)
    settings = ConfigObj(os.path.join(directory, "settings"), interpolation=False)
    settings.update(default)
    settings.pop('templates', '')
    settings.pop('path', '')
    settings.write()
    with open(os.path.join(first_template, 'definition'), 'w') as definition_file:
        definition_file.write(_first_template.DEFINITION)
    with open(os.path.join(first_template, 'new_template'), 'w') as new_template_file:
        new_template_file.write(_first_template.NEW_TEMPLATE)

    return True

def _update_settings_with_config(path, name, default, sections, computed_settings):
    templates_directory = default and os.path.expanduser(default)
    tries = 0
    current_directory = path
    while current_directory and tries < MAX_CONFIG_SEARCH_DEPTH:
        potential_path = os.path.join(current_directory, native_str(name))
        if os.path.isdir(potential_path):
            templates_directory = potential_path
            break

        current_directory = os.path.split(current_directory)[0]
        tries += 1

    if not os.path.isdir(templates_directory):
        create(templates_directory)
    computed_settings['path'] = templates_directory

    templates = {}
    for template_name in glob(os.path.join(templates_directory, '*')):
        if os.path.isdir(template_name):
            templates[template_name] = LocalTemplate(template_name)
    computed_settings['templates'] = templates

    settings_file = os.path.join(templates_directory, "settings")
    if os.path.exists(settings_file):
        computed_settings.update(_read_config_file(settings_file).copy())


@lru_cache()
def _read_config_file(file_path):
    computed_settings = {}
    with open(file_path) as config_file:
        settings = ConfigObj(config_file)
        for key, value in settings.items():
            access_key = key.replace('not_', '').lower()
            existing_value_type = type(default.get(access_key, ''))
            if existing_value_type in (list, tuple):
                existing_data = set(computed_settings.get(access_key, default.get(access_key)))
                if key.startswith('not_'):
                    computed_settings[access_key] = list(existing_data.difference(value.split(",")))
                else:
                    computed_settings[access_key] = list(existing_data.union(value.split(",")))
            elif existing_value_type == bool and value.lower().strip() == "false":
                computed_settings[access_key] = False
            else:
                computed_settings[access_key] = existing_value_type(value)
    return computed_settings

