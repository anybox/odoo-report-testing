import os

from odoo_report_testing.assertions import OdooAssertions
try:
    # from odoo 7.0 to 9.0
    from openerp.tests.common import TransactionCase
except:
    # from odoo 10.0
    from odoo.tests.common import TransactionCase


class TestAssertions(TransactionCase, OdooAssertions):
    """Proof that the high level assertions do work."""

    def setUp(self):
        super(TestAssertions, self).setUp()

    def test_assertImage(self):
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_01.pdf'
        )
        file2 = file1
        expected_output_files = [
            '/tmp/single_page_01_diff.png',
            '/tmp/single_page_01_diff.gif'
        ]
        self.assertEqual(
            None, self.assertImage(file1, file2, output_dir='/tmp/')
        )
        for f in expected_output_files:
            self.assertFalse(os.path.isfile(f))
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_00.pdf'
        )
        self.assertRaises(
            AssertionError, self.assertImage, file1, file2, output_dir='/tmp/'
        )
        for f in expected_output_files:
            self.assertTrue(os.path.isfile(f))
            os.remove(f)
        file2 = 'NonExistsFile'
        self.assertRaises(RuntimeError, self.assertImage, file1, file2)
        file1 = 'NonExistsFile'
        self.assertRaises(RuntimeError, self.assertImage, file1, file2)
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_01.pdf'
        )
        self.assertRaises(RuntimeError, self.assertImage, file1, file2)

    def test_assertPdf(self):
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_01.pdf'
        )
        file2 = file1
        self.assertEqual(
            None,
            self.assertPdf(file1, file2, output_dir='/tmp/')
        )
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_00.pdf'
        )
        self.assertRaises(
            AssertionError, self.assertPdf, file1, file2, output_dir='/tmp/'
        )

        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        file2 = file1
        self.assertEqual(
            None, self.assertPdf(file1, file2, output_dir='/tmp/')
        )
        for filename in [
            'multi_page_diff_p2-p3.pdf',
            'multi_page_diff_p2.pdf',
            'multi_page_diff_pages-p2.pdf',
            'multi_page_diff_pages.pdf'
        ]:
            file2 = os.path.join(
                os.path.dirname(__file__), 'demo', filename
            )
            self.assertRaises(
                AssertionError, self.assertPdf, file1, file2,
                output_dir='/tmp/'
            )

    def test_assertOdooReport(self):
        if hasattr(self, 'env'):
            ref_file = 'technical_guide_report_webkit_v8.pdf'
            webkit_module_id = self.env.ref('base.module_report_webkit').id
        else:
            ref_file = 'technical_guide_report_webkit_v7.pdf'
            webkit_module_id = self.ref('base.module_report_webkit')
        ref_file = os.path.join(
            os.path.dirname(__file__), 'demo', ref_file
        )
        self.assertOdooReport(
            ref_file, 'ir.module.module', 'ir.module.reference',
            [webkit_module_id]
        )
