""" instantly/templates.py

Defines how instantly templates should be displayed and interacted with.

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

from configobj import ConfigObj
from pies.overrides import *


class Template(object):
    __slots__ = ('name', 'label', 'description', 'author', 'license', 'programming_language', 'language',
                 'last_updated', 'arguments', 'directory_additions', 'file_additions', 'scripts', 'extra_data')

    def __init__(self, name, label, description, author, programming_language="Python", language="English",
                 last_updated=None, license=None, arguments=None, directory_additions=None, file_additions=None,
                 scripts=None, **extra_data):
        self.name = name
        self.label = label
        self.description
        self.author = author
        self.license = license
        self.programming_language = programming_language
        self.last_updated = last_updated
        self.language = language
        self.arguments = arguments or {}
        self.directory_additions = directory_additions or {}
        self.file_additions = file_additions or {}
        self.scripts = scripts or {}
        self.extra_data = extra_data

    def __str__(self):
        return ("\n"
                "{name}\n"
                "    Author: {author}\n"
                "    License: {license}\n"
                "    Last Updated: {lastUpdated}\n"
                "    Description:\n"
                "       {description}\n"
                "\n").format(name=self.name, author=self.author, license=self.license, lastUpdated=self.lastUpdated,
                             description=self.description)


class LocalTemplate(Template):
    __slots__ = ('location')

    def __init__(self, location):
        self.location = location
        data = ConfigObj(location, interpolation=False)
        data['name'] = os.path.basename(location)
        if not data.get('label', ''):
            data['label'] = data['name'].title()

        Template.__init__(**data)

    def delete(self):
        try:
            shutil.rmtree(self.location)
        except Exception:
            return False

        return True
