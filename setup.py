# --*- encoding: utf-8 -*--
#from __future__ import print_function
import os
import sys
import platform
from setuptools import setup
from codecs import open # To open the README file with proper encoding

#here = os.path.dirname(os.path.abspath(__file__))
#node_root = os.path.join(here, 'js')
#is_repo = os.path.exists(os.path.join(here, '.git'))

#from distutils import log
#log.set_verbosity(log.DEBUG)
#log.info('setup.py entered')
#log.info('$PATH=%s' % os.environ['PATH'])

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename,  encoding='utf-8') as f:
        return f.read()

setup_args = {
    'name': 'sage-francy',
    'version': readfile("VERSION"),
    'description': 'Francy Widget for representing graphs',
    'long_description': readfile("README.rst"),
    'include_package_data': True,
    'data_files': [],
    'url': 'https://github.com/sagemath/sage-francy',
    'author': 'Odile Bénassy',
    'author_email': 'odile.benassy@u-psud.fr',
    'license': 'GPLv3+',
    'classifiers': [
      # How mature is this project? Common values are
      #   3 - Alpha
      #   4 - Beta
      #   5 - Production/Stable
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Mathematics',
      'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
      'Programming Language :: Python :: 2.7',
    ], # classifiers list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    'keywords': ['SageMath', 'jupyter', 'widget', 'graph'],
    'packages': ['sage_francy'],
    'zip_safe': False,
    'install_requires': ['ipywidgets>=7.0.0', 'networkx', 'jupyter-francy']
}

setup(**setup_args)
