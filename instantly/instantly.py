""" instantly/instantly.py

Defines the basic Python API for interacting with instantly and instant templates

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
import shutil
import tarfile

from configobj import ConfigObj
from pies import *

from . import settings
from .service import Client
from .template import LocalTemplate, RemoteTemplate

DEFAULT_TEMPLATE_PATH = os.environ.get("INSTANT_TEMPLATES_PATH", os.path.expanduser('~') + "/.instant_templates/")


class Instantly(object):

    def __init__(self, run_path=None, settings_search_path=None, **setting_overrides):
        self.run_path = run_path or os.getcwd()
        self.settings = settings.from_path(settings_search_path or self.run_path).copy()
        self.settings.update(setting_overrides)
        self.client = Client(self.settings['path'])

    def _template(self, template_name):
        return self.settings['templates'].get(os.path.join(self.settings['path'], template_name), None)

    def _index_template(self, template_path):
        self.settings['templates'][template_path] = LocalTemplate(template_path)

    @property
    def installed_templates(self):
        return sorted(self.settings['templates'].values(), key=lambda template: template.name)

    def install(self, template_name, look_remotely=True):
        self.uninstall(os.path.basename(template_name))
        if not os.path.isabs(template_name):
            template_name = os.path.join(self.run_path, template_name)

        if os.path.isdir(template_name):
            try:
                shutil.copytree(template_name, self.settings['path'])
                self._index_template(os.path.join(self.settings['path'], template_name))
                return True
            except Exception:
                return False

        return look_remotely and self.download(os.path.basename(template_name))

    def download(self, template_name, template=None):
        template = template or self.client.grab(template_name)
        if not template or not template['template']:
            return False

        self.uninstall(os.path.basename(template_name))
        install_location = os.path.join(self.settings['path'], template_name)
        tar_file_name = install_location + ".tar.gz"
        with open(tar_file_name, "wb") as tar:
            tar.write(template['template'].decode("base64").decode("zlib"))
        tarfile.open(tar_file_name).extractall(self.settings['path'])
        os.remove(tar_file_name)

        definition = ConfigObj(os.path.join(install_location, 'definition'), interpolation=False)
        definition['last_updated'] = template.get('lastUpdated', '')
        definition['author'] = template.get('author', '')
        definition.write()
        self._index_template(install_location)

        return True

    def uninstall(self, template_name):
        template = self.settings['templates'].pop(os.path.join(self.settings['path'], template_name), None)
        if not template:
            return False

        return template.delete()

    def find(self, keyword):
        return [RemoteTemplate(template) for template in self.client.find(keyword)]

    def share(self, template_name):
        return self.client.share(template_name)

    def unshare(self, template_name):
        return self.client.unshare(template_name)

    def expand(self, template_name, arguments):
        return self._template(template_name).expand(self.run_path, arguments)

    def create_settings(self):
        return settings.create(os.path.join(self.run_path, ".instant_templates"))

    def get_template(self, template_name):
        local_template = self._template(template_name)
        if local_template:
            if self.settings['auto_update_templates']:
                matching_template = self.find(template_name)
                if matching_template:
                    matching_template = matching_template[0]
                    if matching_template.author == local_template.author and \
                       (not local_template.last_updated or
                         matching_template.last_updated > local_template.last_updated):
                        self.download(template_name)
                        local_template = self._template(template_name)

            return local_template
        else:
            self.install(template_name, look_remotely=self.settings['auto_update_templates'])
            return self._template(template_name)
