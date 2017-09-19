#!/usr/bin/env python
import os

from setuptools import setup, find_packages


try:
    version_tag = os.environ['VERSION_TAG']
    with open('version', 'w') as version_file:
        version_file.write(version_tag)
except KeyError:
    try:
        with open('version') as version_file:
            version_tag = version_file.read()
    except:
        version_tag = 'dev0'

version = '0.0.1.{0}'.format(
    version_tag
)

install_requires = [
    'setuptools',
    'numpy',
    'pandas',
]

dependency_links = [

]

setup(name='betting_analytics',
      version=version,
      description='DataScience Framework For Betting Analytics',
      author='',
      author_email='',
      url='https://github.com/sashml/betting_analytics',
      packages=find_packages(),
      install_requires=install_requires,
      dependency_links=dependency_links,
      # package_dir={'': '.'},
      package_data={'': ['*.yaml']},
      # namespace_packages=['betting_analytics'],
      entry_points={
          'console_scripts':
              [
              ],
      },
      )
