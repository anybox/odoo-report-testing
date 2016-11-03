Contribute
==========

You can suggest a change by `creating a PR on github <https://help.github.com/
articles/creating-a-pull-request/>`_ against *master* branch.


Setup development environment
-----------------------------

To launch unittest you have to get an odoo instance running, however as far
as I know from odoo launcher you can't run test from files that are not part
of an odoo module.

So let's use nose with the `anybox.recipe.odoo <http://docs.anybox.fr/
anybox.recipe.odoo/current/>`_::

    # create a python virtualenv with no pip/setuptools
    virtualenv -p python2 odoo-sandbox --no-setuptools
    # clone odoo-report-testing repo
    git clone https://github.com/anybox/odoo-report-testing
    cd odoo-report-testing
    # setup buildout
    ../odoo-sandbox/bin/python bootstrap.py
    # setup project according the choosen buildout.cfg
    bin/buildout -c buildout.cfg
    # create an empty pg database
    createdb ort
    # setup ort database with odoo base module
    bin/start_odoo -d ort --stop-after-int -i base
    # launch unittest test of odoo report testing
    bin/nosetests -d ort -- -s -v odoo_report_testing/tests/

Voila!
