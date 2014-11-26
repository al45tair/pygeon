# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst', 'r') as f:
    long_desc = f.read().decode('utf-8')

setup(name='pygeon',
      version='0.1.0',
      description='IP Geolocation in Python',
      long_description=long_desc,
      author='Alastair Houghton',
      author_email='alastair@alastairs-place.net',
      url='http://bitbucket.org/al45tair/pygeon',
      license='MIT License',
      packages=['pygeon'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries',
          'Topic :: System :: Networking'
          ],
      scripts=['scripts/pygeon'],
      install_requires=[
          'sqlalchemy >= 0.9.8',
          'IPy >= 0.82',
          'bintrees >= 2.0.1'
          ],
      provides=['pygeon']
)
