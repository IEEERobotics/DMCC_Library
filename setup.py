import os
from glob import glob
from setuptools import setup, find_packages

# Setup flags and parameters
pkg_name = 'pyDMCC'  # top-level package name

# Cache readme contents for use as long_description
readme = open('README.md').read()

# Call setup()
setup(
  name=pkg_name,
  version='0.1',
  description='Dual Motor Control Cape',
  long_description=readme,
  url='https://github.com/Exadler/DMCC_Library',
  author='Sarah Tan, Paul Tan',
  author_email='support@exadler.com',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  data_files = [ (pkg_name, [pkg_name + "/default_config.json"]) ],
  scripts = glob("examples/*"),
  install_requires=[
    'i2c_device'
  ],
  test_suite=(pkg_name + '.tests'),
  platforms='any',
  keywords='i2c device abstraction development utilities tools',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Programming Language :: Python :: 2.7',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ])
