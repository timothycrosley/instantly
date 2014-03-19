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

from __future__ import absolute_import, division, print_function, unicode_literals

import json
import os
import tarfile
from getpass import getpass

import requests
from configobj import ConfigObj
from pies import *

BASE_URL = "www.instantly.pl"
URL = "http://" + BASE_URL + "/api/"


class Client(object):
    __slots__ = ('_token', '_session', 'template_directory')

    def __init__(self, template_directory):
        self._session = None
        self.template_directory = template_directory

    def _get_authenticated_session(self):
        if not self._session:
            print("Please enter the login credentials for a Google account that has been registered with " + BASE_URL)
            username = raw_input("Username (email): ")
            password = getpass()
            self._session = requests.session()
            google_auth_request = requests.get('https://www.google.com/accounts/ClientLogin',
                                               params={"Email": username, "Passwd":  password, "service": "ah",
                                               "source": BASE_URL, "accountType": "HOSTED_OR_GOOGLE"})
            self._token = dict(item.split("=") for item in google_auth_request.content.split("\n") if item)['Auth']

        return self._session

    def with_authentication(self, api_call, method="post", *kargs, **kwargs):
        session = self._get_authenticated_session()
        session.get('http://www.instantly.pl/_ah/login', params={'continue': URL + api_call, 'auth': self._token})
        return getattr(session, method)(URL + api_call, headers={'Authorization': "Basic %s" % self._token,
                                                                      'Content-Type':'application/json'},
                                             *kargs, **kwargs)

    def without_authentication(self, api_call, method="get", *kargs, **kwargs):
        return getattr(requests, method)(URL + api_call, *kargs, **kwargs)

    def share(self, template_name):
        try:
            template_location = os.path.join(self.template_directory, template_name)
            template = ConfigObj(os.path.join(template_location, "definition"), interpolation=False)
            tarPath = os.path.join(self.template_directory, template_name + ".tar.gz")
            with tarfile.open(tarPath, "w") as tar:
                tar.dereference = True
                tar.add(template_location, arcname=template_name)
            with open(tarPath, 'rb') as tar:
                encoded_template = tar.read().encode("zlib").encode("base64")

            self.with_authentication("InstantTemplate", data=json.dumps({"license":template.get("license", ""),
                                            "name":template_name, "description":template.get("description", ""),
                                            "template":encoded_template}))
            os.remove(tarPath)
        except Exception:
            return False

        return True

    def find(self, search_term):
        return self.without_authentication("find/%s" % search_term).json()

    def grab(self, template_name):
        template = self.without_authentication("InstantTemplate/%s" % template_name)
        if not template:
            return None

        return template.json()

    def unshare(self, template_name):
        try:
            return self.with_authentication("InstantlyTemplate", data={'name': template_name}, method="delete")
        except Exception:
            return False
