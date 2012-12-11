#!/usr/bin/env python

from distutils.core import setup

setup(name='Instantly',
      version='0.2',
      description='A tool which allows you to create templates that can be expanded into full projects or stubs instantly.',
      author='Timothy Crosley',
      author_email='timothy.crosley@gmail.com',
      url='http://www.simpleinnovation.org/',
      download_url='https://github.com/timothycrosley/Instantly/blob/master/dist/Instantly-0.2.tar.gz?raw=true',
      license = "GNU GPLv2",
      scripts=['scripts/instantly',],
      requires = ['configobj', 'rest'],
      package_data={'InstantlyFiles': ["instant_templates/create_instant_template/*"]},
      include_package_data=True,
      packages=['InstantlyFiles',],)
