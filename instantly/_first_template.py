""" instantly/_first_template.py

Defines the first template to be included with every new installation of instantly: a template that enables creating
new templates instantly!

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

DEFINITION = """label = "Instant Template"
description = "Adds a new instant template to the list of options to be created."
icon = "Add"
license = "MIT"
author = "timothy.crosley@gmail.com"

[Arguments]
    [[label]]
    prompt = "Label"
    type = "string"
    help_text = "The displayed label for you new instant template [ie: Instant Template]"
    [[name]]
    prompt = "Name"
    type = "string"
    help_text = "The action name of your template used to expand from the console [ie: create_instant_template]"
    [[description]]
    prompt = "Description"
    type = "string"
    help_text = "The displayed description for your new instant template [ie: Adds a new instant template...]"

[DirectoryAdditions]
new_template_directory = "{INSTANTLY::InstantTemplates}/{INSTANTLY::name}/"

[FileAdditions]
new_template = "{INSTANTLY::new_template_directory}/definition"
"""

NEW_TEMPLATE = """label = "{INSTANTLY::label}"
name = "{INSTANTLY::name}"
description = "{INSTANTLY::description}"
icon = "Default"
license = "GPLV2"

[Arguments]
# Put inputs you want to gather from the user, along with the explanation presented to the user here. IE:
#      [[name]]
#       prompt = "Name"
#       type = "string"
#       default = "hi"

[DirectoryAdditions]
# Put directories you want created here. IE:
#       NewDirectory = /creat/this/directory/
# Hint: you can than add files to that directory in FileAddition reusing the definition: percent(NewDirectory)s


[FileAdditions]
# Put the source template files here along with there eventual destination. All source templates must be in the same
# directory as the definition file. IE:
#      TemplateSource.py = /expand/to/this/directory/creating/directories/as/needed/along/the/way/destination

[Scripts]
# Put triggered scripts here. IE:
#      onfinish = "wall 'We are done!'",
"""
