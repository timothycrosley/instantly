#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

from distutils.core import setup

from pies.overrides import *

setup(name='Instantly',
      version='0.8.3',
      description='A tool which allows you to create templates that can be expanded into full projects or stubs instantly.',
      author='Timothy Crosley',
      author_email='timothy.crosley@gmail.com',
      url='http://www.simpleinnovation.org/',
      download_url='https://github.com/timothycrosley/Instantly/blob/master/dist/Instantly-0.8.3.tar.gz?raw=true',
      license = "GNU GPLv2",
      scripts=['scripts/instantly',],
      requires=['configobj', 'rest', 'pies>=2.0.0'],
      install_requires=['configobj', 'rest', 'pies>=2.0.0'],
      package_data={'InstantlyFiles': ["instant_templates/create_instant_template/*"]},
      include_package_data=True,
      packages=['InstantlyFiles',],)
