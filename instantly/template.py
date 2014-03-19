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
from datetime import datetime
from subprocess import Popen

from configobj import ConfigObj
from pies.overrides import *


class Template(object):
    __slots__ = ('name', 'label', 'description', 'author', 'license', 'programming_language', 'language',
                 'last_updated', 'arguments', 'directory_additions', 'file_additions', 'scripts', 'finish_message',
                 'extra_data')

    def __init__(self, name, label="", description="", author="", programming_language="N/A", language="English",
                 last_updated=None, license=None, arguments=None, directory_additions=None, file_additions=None,
                 scripts=None, finish_message="", **extra_data):
        if last_updated:
             last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M")

        self.name = name
        self.label = label
        self.description = description
        self.author = author
        self.license = license
        self.programming_language = programming_language
        self.last_updated = last_updated
        self.language = language
        self.arguments = arguments or {}
        self.directory_additions = directory_additions or {}
        self.file_additions = file_additions or {}
        self.scripts = scripts or {}
        self.finish_message = finish_message
        self.extra_data = extra_data

    def __repr__(self):
        return self.name

    def __str__(self):
        return ("\n"
                "{name}\n"
                "    Author: {author}\n"
                "    License: {license}\n"
                "    Last Updated: {lastUpdated}\n"
                "    Description:\n"
                "       {description}\n"
                "\n").format(name=self.name, author=self.author, license=self.license, lastUpdated=self.last_updated,
                             description=self.description)


class LocalTemplate(Template):
    __slots__ = ('location')

    def __init__(self, location):
        self.location = location
        data = ConfigObj(os.path.join(location, 'definition'), interpolation=False)
        data['name'] = os.path.basename(location)
        if not data.get('label', ''):
            data['label'] = data['name'].title()

        data['scripts'] = data.pop('Scripts', {})
        data['directory_additions'] = data.pop('DirectoryAdditions', {})
        data['file_additions'] = data.pop('FileAdditions', {})
        data['arguments'] = data.pop('Arguments', {})

        Template.__init__(self, **data)

    def delete(self):
        try:
            shutil.rmtree(self.location)
        except Exception:
            return False

        return True

    def make_substitutions(self, string, substitutions):
        for name, value in substitutions.items():
            string = string.replace("{INSTANTLY::" + str(name) + "}", str(value))

        return string

    def expand(self, path, arguments):
        substitutions = dict(InstantTemplates="/" + os.path.dirname(self.location.strip("/")),
                             current_date=datetime.now())
        substitutions.update(os.environ)
        substitutions.update(arguments)

        beforerun = self.scripts.get('beforerun', [])
        if beforerun:
            print("This script wants to perform the following command line actions:")
            print("    -" + "\n    -".join(beforerun))
            print("")
            if input("Is this okay (Y/N)?").lower() in ('y', 'yes'):
                for script in beforerun:
                    Popen(self.make_substitutions(script, substitutions), shell=True).wait()

        for name, directory in itemsview(self.directory_additions):
            directory = self.make_substitutions(directory, substitutions)
            if not os.path.isabs(directory):
                directory = os.path.join(path, directory)
            substitutions[name] = directory
            try:
                defined_directory = os.path.join(self.location, name)
                if os.path.isdir(defined_directory):
                    if os.path.isdir(directory):
                        shutil.rmtree(directory)
                    shutil.copytree(defined_directory, directory)
                else:
                    os.makedirs(directory)
            except:
                pass

        for source, destination in itemsview(self.file_additions):
            with open(os.path.join(self.location, source)) as in_file:
                destination = self.make_substitutions(destination, substitutions)
                if not "::" in destination:
                    (out_file_name, mode) = (destination, "")
                else:
                    (out_file_name, mode) = destination.split("::")
                if not os.path.isabs(out_file_name):
                    out_file_name = os.path.join(path, out_file_name)
                substitutions[source] = out_file_name

                out_directory = os.path.dirname(out_file_name)
                if not os.path.exists(out_directory):
                    os.makedirs(out_directory)

                in_file_content = in_file.read()
                for substitutionName, substitionValue in substitutions.items():
                    in_file_content = self.make_substitutions(in_file_content, substitutions)

                if mode == "APPEND":
                    with open(out_file_name, 'a') as out_file:
                        out_file.write(in_file_content)
                elif mode.startswith("REPLACE"):
                    toReplace = mode[8:]
                    with open(out_file_name, 'r') as currentFile:
                        currentFileContents = currentFile.read()
                        with open(out_file_name, 'w') as out_file:
                            out_file.write(currentFileContents.replace(toReplace, in_file_content))
                elif mode.startswith("BEFORE"):
                    placement = mode[7:]
                    with open(out_file_name, 'r') as currentFile:
                        currentFileContents = currentFile.read()
                        with open(out_file_name, 'w') as out_file:
                            out_file.write(currentFileContents.replace(placement, in_file_content + "\n" + placement))
                elif mode.startswith("AFTER"):
                    placement = mode[6:]
                    with open(out_file_name, 'r') as currentFile:
                        currentFileContents = currentFile.read()
                        with open(out_file_name, 'w') as out_file:
                            out_file.write(currentFileContents.replace(placement, placement + "\n" + in_file_content))
                else:
                    with open(out_file_name, 'w') as out_file:
                        out_file.write(in_file_content)

        onfinish = self.scripts.get('onfinish', [])
        if onfinish:
            onfinish = [self.make_substitutions(item, substitutions) for item in onfinish]
            print("This script wants to perform the following command line actions:")
            print("    -" + "\n    -".join(onfinish))
            print("")
            if input("Is this okay (Y/N)?").lower() in ('y', 'yes'):
                for script in onfinish:
                    Popen(script, shell=True).wait()

        return True


class RemoteTemplate(Template):
    __slots__ = ()

    def __init__(self, template):
        template['last_updated'] = template.pop('lastUpdated', '')
        Template.__init__(self, **template)
