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

from .instantly import Instantly


def main():
    instantly = Instantly()
    if not len(sys.argv) > 1:
        print("Instantly allows you to expand simple templates, that take in a set number of arguments")
        print("Usage: instantly [template name] to expand a template")
        print("       type instantly help for full instructions.")
        print("")
        print("Installed Templates:")
        print("\t" + str(templates))
        sys.exit(1)

    command = sys.argv[1]
    extraInputs = sys.argv[2:]
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
        print("instantly uninstall [template name]")
        print("\t Permanently removes an installed template locally")
        print("instantly create_instant_template")
        print("\t Create a new instant template to automate a task")
        print("instantly share [template name]")
        print("\t Share a template you have created with others online")
        print("\t Must register your google account with http://instantly.pl/ to do this")
        print("instantly unshare [template name]")
        print("\t Removes a template that you previously shared from the instantly online repository.")
        print("instantly install [template directory]")
        print("\t Installs an instant_template directory from the local file system "
              "or online repository into your personal collection of templates")
        sys.exit(0)
    elif command == "uninstall":
        template_name = sys.argv[2]
        if raw_input("Are you sure you want to delete %s (y/n)? " % template_name).lower() in ("y", "yes"):
            if instantly.uninstall(template_name):
                print("Successfully removed %s from local templates" % template_name)
        sys.exit(0)
    elif command == "share":
        template_name = sys.argv[2]
        template = ConfigObj(TEMPLATE_PATH + template_name + "/definition", interpolation=False)
        client = createClient()
        tarPath = TEMPLATE_PATH + template_name + ".tar.gz"
        with tarfile.open(tarPath, "w") as tar:
            tar.dereference = True
            tar.add(TEMPLATE_PATH + template_name, arcname=template_name)
        with open(tarPath, 'rb') as tar:
            encodedTemplate = tar.read().encode("zlib").encode("base64")

        client.post("InstantTemplate", {"license":template["Info"].get("license", ""),
                                        "name":template_name, "description":template["Info"].get("description", ""),
                                        "template":encodedTemplate})
        os.remove(tarPath)
        print("Successfully shared %s, thanks for helping to expand the number of instant templates!" % template_name)
        sys.exit(0)
    elif command == "find":
        searchTerm = sys.argv[2]
        results = createClient(authenticated=False).get("find/%s" % searchTerm)
        if not results:
            print("Sorry: no templates have been shared that match the search term '%s'," % searchTerm)
            print("       but you could always add one ;)")
            sys.exit(0)

        print("Instantly found the following templates:")
        for result in results:
            print(TEMPLATE_DESCRIPTION % result)

        print(" To install one of these templates run: instantly grab [template_name]")
        sys.exit(0)
    elif command == "grab":
        template_name = sys.argv[2]
        template = createClient(authenticated=False).get("InstantTemplate/%s" % template_name)
        if not template:
            print("Sorry: no one has thought of a way to instantly '%s'," % searchTerm)
            print("       but you could always create one ;)")
            sys.exit(0)
        tarPath = TEMPLATE_PATH + template_name + ".tar.gz"
        with open(tarPath, "wb") as tar:
            tar.write(template['template'].decode("base64").decode("zlib"))
        tarfile.open(tarPath).extractall(TEMPLATE_PATH)
        os.remove(tarPath)

        print("%(name)s has been installed as a local template. Run 'instantly %(name)s' to expand it." % \
            {"name":template_name})
        sys.exit(0)


if __name__ == "__main__":
    main()
