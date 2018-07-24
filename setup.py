#!/usr/bin/env python
import os

from setuptools import setup, find_packages


install_requires = [
    'setuptools',
    'numpy',
    'pandas',
]

dependency_links = [
    
]

setup(name='betting_analytics',
      version=0.1,
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
