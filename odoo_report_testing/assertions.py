"""High level Odoo assertions."""
import os
from .reports import pdftools


class OdooAssertions(object):
    """Mixin class providing assertion and helper methods to write tests.
    """

    def assertImage(self, ref, compared, msg=None, output_dir=None):
        """Test if two images are equals, if not, this generate a diff file and
        a animated gif file to highlight differences.

        It could be two single page pdf files.

        This delegate the work to ``compare`` application installed with
        **imagemagick** package which is required.

        :param ref: a ``path`` to the file used as reference, expected result
        :param compared: a ``path`` to the file to compare to the ref file.
        :param msg: A message to print in case of faillure
        :output_dir: Directory to generate diff files
        """
        diff = pdftools.imagediff(ref, compared, output_dir)
        if diff.get('equal'):
            for f in diff.get('diff_files'):
                os.remove(f)
        else:
            message = msg if msg else """Compared file %(compared)r is different from
                                         its reference %(ref)r,
                                         Find out differences in diff files (
                                         %(diff_files)r))"""
            self.fail(message % dict(ref=ref, compared=compared,
                                     diff_files=diff.get('diff_files')))

    def assertPdf(self, ref, compared, msg=None, output_dir=None):
        """Test if two pdf are equals

        This split the pdf and delegate the assertion to assertImageEquals.

        To split the pdf ``pdftk`` application from **pdftk** package is
        required.
        """
        diff = pdftools.pdfdiff(ref, compared, output_dir)
        for page in diff.get('pages'):
            if page.get('equal'):
                os.remove(page.get('reference'))
                os.remove(page.get('compared'))
                for f in page.get('diff_files'):
                    os.remove(f)
        if not diff.get('equal'):
            message = msg if msg else \
                u"Compared file %(compared)r is different from its " \
                u"reference %(ref)r.\n" \
                u"Look at diff files to quickly show differences."
            self.fail(message % dict(ref=ref, compared=compared, ))

    def assertOdooReport(
        self, reference, model, report_service_name, ids, data={}, context=None
    ):
        """Generate report and compare to a reference file, test will failed if
        files are different, have a look close to the reference file you will
        find a diff picture that show you differences.

        here an example to test sale order quotation report::

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

        .. warning::

            You may want to generate those report without expose any odoo port
            so that you can render report properly without http access.

            You can follow this PR:
             - `anybox/odoo <https://github.com/anybox/odoo/pull/12>`_

        :param reference: Path to the report that the generated report should
                          looks like
        :param model: fully qualified model name
        :param report_service_name: report name (without `report.`)
        :param ids: object used to generate the report
        :param data: extra data given to draw the report
        :param context: odoo context
        """
        if hasattr(self, 'env'):
            version7 = False
        else:
            version7 = True
        report, format = pdftools.generateReport(
            self.cr, self.uid, model, report_service_name, ids, data=data,
            context=context, version7=version7
        )
        if format != 'pdf':
            raise Exception("AssertOdooReport work only with pdf files.")
        directory, filename = pdftools.outputs_env(reference)
        generated = os.path.join(directory, filename + '_generated.pdf')
        with open(generated, 'wb') as report_file:
            report_file.write(report)
        self.assertPdf(reference, generated)
