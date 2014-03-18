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

from pies import *

from . import settings
from .service import Client

DEFAULT_TEMPLATE_PATH = os.environ.get("INSTANT_TEMPLATES_PATH", os.path.expanduser('~') + "/.instant_templates/")

class Instantly(object):

    def __init__(self, run_path=None, **setting_overrides):
        self.run_path = run_path or os.getcwd()
        self.settings = settings.from_path(self.run_path).copy()
        self.settings.update(setting_overrides)
        self.client = Client(self.settings['path'])

    @property
    def installed_templates(self):
        return self.settings.templates

