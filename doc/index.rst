.. pygeon documentation master file, created by
   sphinx-quickstart on Wed Nov 26 13:12:53 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pygeon - Pythonic geolocation
=============================

This document refers to version |release|

What is this?
=============

`pygeon` is a Python module that implements simple IP geolocation for both
IPv4 and IPv6.  It doesn’t rely on third-party databases that might not be
maintained, but instead fetches the necessary data directly from RIPE’s FTP
server.

Usage
=====

`pygeon` installs a script that you can use from the command line; e.g.::

  $ pygeon -d sqlite:////tmp/ipranges.sqlite3 update
  Found 82649 ranges
  $ pygeon -d sqlite:////tmp/ipranges.sqlite3 134.170.185.46
  US

It also provides a Python API that you can use in your own programs::

  >>> import pygeon
  >>> store = pygeon.SQLAlchemyStore('sqlite:////tmp/ipranges.sqlite3')
  >>> geo = pygeon.Geolocator(store)
  >>> iprange = geo.lookup('134.170.185.46')
  >>> print iprange.start
  134.170.0.0
  >>> print iprange.country
  US

Code Documentation
==================

Contents:

.. toctree::
   :maxdepth: 2

   pygeon


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

