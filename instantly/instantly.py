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

from pies import *

from . import settings
from .service import Client
from .template import LocalTemplate

DEFAULT_TEMPLATE_PATH = os.environ.get("INSTANT_TEMPLATES_PATH", os.path.expanduser('~') + "/.instant_templates/")

class Instantly(object):

    def __init__(self, run_path=None, **setting_overrides):
        self.run_path = run_path or os.getcwd()
        self.settings = settings.from_path(self.run_path).copy()
        self.settings.update(setting_overrides)
        self.client = Client(self.settings['path'])

    def _index_template(self, template_path):
        self.templates[template_path] = LocalTemplate(template_path)

    @property
    def installed_templates(self):
        return sorted(self.settings.templates.values(), key=lambda template: template.name)

    def install(self, template_name):
        self.remove(os.path.basename(template_name))
        if not os.path.isabs(template_name):
            template_name = os.path.join(self.run_path, template_name)

        if os.path.isdir(template_name):
            try:
                shutil.copytree(template_name, self.settings.path)
                return True
            except Exception:
                return False

        return self.download(template_name)

    def download(self, template_name):
        template = client.grab(template_name)
        if not template:
            return False

        self.remove(os.path.basename(template_name))
        tar_file_name = os.path.join(self.settings.path, templateName + ".tar.gz")
        with open(tar_file_name, "wb") as tar:
            tar.write(template['template'].decode("base64").decode("zlib"))
        tarfile.open(tar_file_name).extractall(TEMPLATE_PATH)
        os.remove(tar_file_name)

        return True

    def remove(self, template_name):
        template = settings.templates.pop(os.path.join(self.settings.path, template_name), None)
        if not template:
            return False

        return template.delete()
