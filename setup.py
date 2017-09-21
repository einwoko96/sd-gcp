# setup.py
from setuptools import setup, find_packages

setup(name='train.py',
  version='0.1',
  packages=find_packages(),
  description='lstm training module',
  author='Jacob Freeman',
  author_email='jhfreeman@utexas.edu',
  license='MIT',
  install_requires=[
      'keras',
      'h5py',
      'tqdm',
      'pandas'
  ],
  zip_safe=False)
