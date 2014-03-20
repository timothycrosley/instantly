#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
   import pypandoc
   readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, OSError, RuntimeError):
   readme = ''

setup(name='instantly',
      version='1.0.0',
      description='A tool which allows you to create templates that can be expanded into full projects or stubs '
                  'instantly.',
      long_description=readme,
      author='Timothy Crosley',
      author_email='timothy.crosley@gmail.com',
      url='http://www.instantly.pl/',
      download_url='https://github.com/timothycrosley/instantly/archive/1.0.0.tar.gz',
      license = "MIT",
      requires=['configobj', 'requests', 'pies'],
      install_requires=['configobj', 'requests', 'pies>=2.6.1'],
      packages=['instantly',],
      entry_points={
        'console_scripts': [
            'instantly = instantly.main:main',
        ]
      },
      keywords='Accelerate, Python, Python2, Python3, Templating, Automate, Template, Snippet',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Environment :: Console',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.0',
                   'Programming Language :: Python :: 3.1',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities'],)
