# setup.py
from setuptools import setup, find_packages

setup(name='train.py',
  version='0.1',
  packages=find_packages(),
  description='example to run keras on gcloud ml-engine',
  author='Jacob Freeman',
  author_email='jhfreeman@utexas.edu',
  license='MIT',
  install_requires=[
      'keras',
      'h5py'
  ],
  zip_safe=False)
