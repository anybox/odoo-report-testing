===================
Odoo report testing
===================

This lib provide tools to test odoo reports from version 7 and higher.


.. image:: https://api.travis-ci.org/anybox/odoo-report-testing.svg?branch=master
    :target: https://travis-ci.org/anybox/odoo-report-testing
    :alt: Travis state

.. image:: https://readthedocs.org/projects/odoo-report-testing/badge/?version=master
    :target: https://odoo-report-testing.readthedocs.io/en/latest
    :alt: Documentation Status


Configuration
=============

It's encouraged to not install this tool and dependences in a production server.

In order to properly compare images with ImageMagick make sure you have configure
the following policy in ``/etc/ImageMagick-6/policy.xml``:

.. code::

  -  <policy domain="coder" rights="none" pattern="PDF" />
  +  <policy domain="coder" rights="read | write" pattern="PDF" />

Taking this security issue in consideration: https://www.kb.cert.org/vuls/id/332928/ 

Resources
=========

- `Documentation <https://odoo-report-testing.readthedocs.io>`_
- `Issue Tracker <https://github.com/anybox/odoo-report-testing/issues>`_
- `Code <https://github.com/anybox/odoo-report-testing/>`_


Licence
=======

.. image:: https://www.gnu.org/graphics/agplv3-155x51.png
    :target: https://www.gnu.org/licenses/agpl.txt
    :alt: The GNU Affero General Public License v3
