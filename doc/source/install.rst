Install
=======

We are going to see in details what are dependencies then various way to
install this library:

* with pip
* from code source
* using a buildout configuration

External requirements
---------------------

This library call ``compare`` from ``imagemagick`` to compare 2 (one page) pdf
bit to bit. ``pdftk`` is used to split multi page pdf file into multiple single
page pdf files.

To install those dependecies on a debian based system::

    $ sudo aptitude install imagemagick pdftk

Install Odoo report testing
---------------------------

Using pip
~~~~~~~~~
The latest release pushed on pypi can be installed using pip::

    pip install odoo-report-testing

Refer to `the pip user guide <https://pip.pypa.io/en/stable/user_guide/>`_
for an advanced usage of pip!

Using anybox recipe odoo
~~~~~~~~~~~~~~~~~~~~~~~~

Here a simple example of odoo 8 configuration::

    [buildout]
    parts = odoo
    versions = versions
    # Un-comment following 2 lines if you want to hack odoo report testing
    # in your current project
    # extensions = gp.vcsdevelop
    # vcs-extend-develop = git+https://github.com/anybox/odoo-report-testing@master#egg=odoo-report-testing

    [odoo]
    recipe = anybox.recipe.odoo:server
    version = git http://github.com/anybox/odoo.git ocb 8.0-render_report_offline
    addons = local my_addons

    openerp_scripts = nosetests=nosetests command-line-options=-d

    eggs =
        odoo-report-testing
        anybox.recipe.odoo
        nose
        coverage
        soappy
        PyPDF
        pysftp

    [versions]
    psutil = 2.2.1
    feedparser = 5.1.3
    paramiko = 1.16.0
    gevent = 1.0.2
    pysftp = 0.2.8
    wstools = 0.4.3

