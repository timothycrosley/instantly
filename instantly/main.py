""" instantly/main.py

Defines the basic terminal interface for interacting with Instantly.

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

import sys

from pies.overrides import *

from .instantly import Instantly

TYPE_MAP = {'string': str, 'str': str, 'int': int, 'bool': bool}


def main():
    instantly = Instantly()
    if not len(sys.argv) > 1:
        print("Instantly allows you to expand simple templates, that take in a set number of arguments")
        print("Usage: instantly [template name] to expand a template")
        print("       type instantly help for full instructions.")
        print("")
        print("Installed Templates:")
        print("\t" + str(instantly.installed_templates))
        sys.exit(1)

    command = sys.argv[1]
    template_name = sys.argv[2:3] and sys.argv[2] or ""
    extra_inputs = sys.argv[2:]
    if command == "help":
        print("Instantly Commands")
        print("")
        print("instantly [template name]")
        print("\t Expand the named template")
        print("instantly help")
        print("\t Get full list of commands / help text")
        print("instantly find [template name]")
        print("\t Find pre-made templates to automate a task online")
        print("instantly download [template name]")
        print("\t Add a template shared online to your local template repository")
        print("instantly install [template directory]")
        print("\t Installs an instant_template directory from the local file system "
              "or online repository into your personal collection of templates")
        print("instantly uninstall [template name]")
        print("\t Permanently removes an installed template locally")
        print("instantly create_instant_template")
        print("\t Create a new instant template to automate a task")
        print("instantly share [template name]")
        print("\t Share a template you have created with others online")
        print("\t Must register your google account with http://instantly.pl/ to do this")
        print("instantly unshare [template name]")
        print("\t Removes a template that you previously shared from the instantly online repository.")
        print("instantly create_settings [template directory]")
        print("\t Will create an alternate settings / template directory within the current directory.")
        sys.exit(0)
    elif command == "uninstall":
        if input("Are you sure you want to delete %s (y/n)? " % template_name).lower() in ("y", "yes"):
            if instantly.uninstall(template_name):
                print("Successfully removed %s from local templates" % template_name)
                sys.exit(0)
            else:
                sys.exit(1)
    elif command == "share":
        if instantly.share(template_name):
            print("Successfully shared %s, thanks for helping to expand the number of instant templates!" % template_name)
            sys.exit(0)
        else:
            sys.exit(1)
    elif command == "unshare":
        if instantly.unshare(template_name):
            print("Successfully un-shared %s!" % template_name)
            sys.exit(0)
        else:
            sys.exit(1)
    elif command == "create_settings":
        if instantly.create_settings():
            print("Successfully created a new settings / templates directory!")
            sys.exit(0)
        else:
            sys.exit(1)
    elif command == "find":
        results = instantly.find(template_name)
        if not results:
            print("Sorry: no templates have been shared that match the search term '%s'," % template_name)
            print("       but you could always add one ;)")
            sys.exit(0)

        print("Instantly found the following templates:")
        for result in results:
            print(result)

        print(" To install one of these templates run: instantly install [template_name]")
        sys.exit(0)
    elif command == "install":
        if instantly.install(template_name):
            print("%(name)s has been installed as a local template. Run 'instantly %(name)s' to expand it." % \
                  {"name":template_name})
            sys.exit(0)
        else:
            print("Sorry: no one has thought of a way to instantly '%s'," % searchTerm)
            print("       but you could always create one ;)")
            sys.exit(0)
    else:
        template_name = command
        template = instantly.get_template(template_name)
        if not template_name:
            print("Sorry: no one has thought of a way to instantly '%s'," % searchTerm)
            print("       but you could always create one ;)")
            sys.exit(1)

        print("Expanding the following template:")
        print(template)
        arguments = {}
        for argument, argument_definition in itemsview(template.arguments):
            print("")
            if extra_inputs:
                arguments[argument] = extra_inputs.pop(0)
            else:
                argument_type = argument_definition.get('type', 'string')
                default = instantly.settings['defaults'].get(argument, '') or argument_definition.get('default', '')
                help_text = argument_definition.get('help_text')
                if help_text:
                    print("Help Text: {0}".format(help_text))

                prompt = argument_definition.get('prompt', '')
                if default:
                    prompt += " [Default: {0}]" + default
                if argument_type == "bool":
                    prompt += " (y/n)"
                prompt += ": "

                value = ""
                while value == "":
                    value = input(prompt)
                    if argument_type == "bool":
                        if value.lower() in ("y", "yes"):
                            value = True
                        elif value.lower() in ("n", "no"):
                            value = False
                        else:
                            value = ""
                    elif argument_type == "int":
                        if value.isdigit():
                            value = int(value)
                        else:
                            value = ""
                arguments[argument] = value

        if instantly.expand(template_name, arguments):
            print("Successfully ran '{0}'!".format(template_name))
            if template.finish_message:
                print(template.finish_message)

if __name__ == "__main__":
    main()
