===================================
Odoo Report Testing's documentation
===================================

This lib provide tools to test odoo reports from version 7 and higher.


Resources
=========

- `Documentation <https://odoo-report-testing.readthedocs.io>`_
- `Issue Tracker <https://github.com/anybox/odoo-report-testing/issues>`_
- `Code <https://github.com/anybox/odoo-report-testing/>`_


Requirements
============

* ``imagemagick`` is used to compare 2 (one page) pdf bit to bit.
* ``pdftk`` is used to split pdf page per page.
* Install this package (with pip ``pip install odoo-report-testing``)

Quickstart
==========

Here an example to test sale order quotation report ``test_so_report.py``::

        # -*- coding: utf-8 -*-
        import os
        from openerp.tests.common import TransactionCase
        from odoo_report_testing.assertions import OdooAssertions



        class TestSoReport(TransactionCase, OdooAssertions):

            def test_simple_so_report(self):
                self.assertOdooReport(
                    os.path.join(
                        os.path.dirname(__file__),
                        'expected_reports',
                        'test_so_report.pdf'
                    ),
                    'sale.order',
                    'sale.report_saleorder',
                    [self.ref('sale.sale_order_1')],
                    data={},
                    context=None
                )

Assuming your module looks like::

    my_module
    ├── test
    │   ├── expected_reports
    │   │   └── test_so_report.pdf
    │   ├── __init__.py
    │   └── test_so_report.py

.. warning::

    You may want to generate those report without expose any odoo port
    so that you can render report properly without http access.

    You can have a look to one of the following PRs:
     - `oca/odoo <https://github.com/odoo/odoo/pull/13656>`_
     - `oca/ocb <https://github.com/OCA/OCB/pull/550>`_
     - `anybox/odoo <https://github.com/anybox/odoo/pull/12>`_


Contents
========

.. toctree::
    :maxdepth: 2

    install
    apidoc
