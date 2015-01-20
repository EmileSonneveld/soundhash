#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


from distutils.core import setup



setup(
    name='soundhash',
    version='0.2',
    description='let your hashes sing!',
    author='Emile Sonneveld',
    author_email='emile.jnm@gmail.com',
    url='https://gist.github.com/EmileSonneveld/7e7053068fd481729b91',
    long_description=open('README.rst').read(),
    packages=['soundhash'],
)
