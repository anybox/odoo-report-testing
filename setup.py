# -*- coding: utf-8 -*-
import io
from setuptools import setup


def parse_requirements(file):
    required = []
    with open(file) as f:
        for req in f.read().splitlines():
            if not req.strip().startswith('#'):
                required.append(req)
    return required


def read(*args, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in args:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


requires = parse_requirements('requirements.txt')
long_description = read('README.rst', 'CHANGES.rst')

setup(
    name="odoo-report-testing",
    version='0.1',
    author="Odoo Community Association (OCA)",
    author_email="support@odoo-community.org",
    summary="Report testing for Odoo",
    license="AGPLV3",
    home_page="https://github.com/OCA/odoo-report-testing",
    url='https://github.com/anybox/selenium-configurator',
    packages=[
        'odoo_report_testing',
    ],
    install_requires=requires,
    tests_require=requires + ['nose'],
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        'License :: OSI Approved :: GNU Affero General Public License v3 or '
        'later (AGPLv3+)',
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Operating System :: POSIX :: Linux",
    ],
)
