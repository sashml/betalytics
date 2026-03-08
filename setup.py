#!/usr/bin/env python
import os

from setuptools import setup, find_packages


install_requires = [
    'setuptools',
    'numpy',
    'pandas',
    'requests',
    'openpyxl',
    'seaborn'
]

dependency_links = [
    
]

setup(name='betalytics',
      version=0.3,
      description='DataScience Framework For Betting Analytics',
      author='',
      author_email='',
      url='https://github.com/sashml/betalytics',
      packages=find_packages(),
      install_requires=install_requires,
      dependency_links=dependency_links,
      package_data={'': ['*.yaml']},
      entry_points={
          'console_scripts':
              [
              ],
      },
      )
