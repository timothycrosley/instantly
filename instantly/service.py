""" instantly/service.py

Defines the interaction between the Google AppEngine hosted Instantly service and the terminal client.

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

import os
import tarfile

import requests
from configobj import ConfigObj

BASE_URL = "www.instantly.pl"
URL = "http://" + BASE_URL + "/api/"


class Client(object):
    __slots__ = ('_token', '_session', 'template_directory')

    def __init__(self, template_directory=None):
        self._session = None
        self.template_directory = template_directory

    def _get_authenticated_session(self):
        if not self._session:
            print("Please enter the login credentials for a Google account that has been registered with " + BASE_URL)
            username = raw_input("Username (email): ")
            password = getpass()
            self._session = requests.session()
            requests.get('https://www.google.com/accounts/ClientLogin',
                         params={"Email": username, "Passwd":  password, "service": "ah",
                                 "source": BASE_URL, "accountType": "HOSTED_OR_GOOGLE"})
            self._token = dict(item.split("=") for item in google_auth_request.content.split("\n") if item)['Auth']

        return self._session

    def with_authentication(self, api_call, method="post", *kargs, **kwargs):
        self.session = self._get_authenticated_session()
        self.session.get('http://www.instantly.pl/_ah/login', params={'continue': URL + api_call, 'auth': self._token})
        return getattr(self.session, method)(API + api_call, headers={'Authorization': "Basic %s" % google_token,
                                                                      'Content-Type':'application/json'},
                                             *kargs, **kwargs)

    def without_authentication(self, api_call, method="get", *kargs, **kwargs):
        return getattr(requests, method)(API + api_call, *kargs, **kwargs)

    def share_template(self, template_name):
        try:
            template = ConfigObj(self.template_directory + template_name + "/definition", interpolation=False)
            tarPath = self.template_directory + template_name + ".tar.gz"
            with tarfile.open(tarPath, "w") as tar:
                tar.dereference = True
                tar.add(self.template_directory + template_name, arcname=template_name)
            with open(tarPath, 'rb') as tar:
                encoded_template = tar.read().encode("zlib").encode("base64")

            client.post("InstantTemplate", {"license":template["Info"].get("license", ""),
                                            "name":templateName, "description":template["Info"].get("description", ""),
                                            "template":encoded_template})
            os.remove(tarPath)
        except Exception:
            return False

        return True

    def find(self, search_term):
        return self.without_authentication("find/%s" % search_term).json

    def grab(self, template_name, template_path):
        template = self.without_authentication("InstantTemplate/%s" % template_name)
        if not template:
            return False

        tar_path = template_path + template_name + ".tar.gz"
        with open(tar_path, "wb") as tar:
            tar.write(template['template'].decode("base64").decode("zlib"))
        tarfile.open(tar_path).extractall(TEMPLATE_PATH)
        os.remove(tar_path)

        return True





