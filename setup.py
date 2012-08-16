#!/usr/bin/env python

from distutils.core import setup

setup(name='Instantly',
      version='0.1',
      description='A drag and drop interface to create WebElement templates quickly and easily.',
      author='Timothy Crosley',
      author_email='timothy.crosley@gmail.com',
      url='http://www.simpleinnovation.org/',
      download_url='https://github.com/timothycrosley/Instantly/blob/master/dist/Instantly-0.1.tar.gz?raw=true',
      license = "GNU GPLv2",
      scripts=['scripts/instantly',],
      requires = ['configobj',],
      package_data={'InstantlyFiles': ["InstantlyFiles/instant_templates/create_instant_template/*"]},
      include_package_data=True,
      packages=['InstantlyFiles',],)
