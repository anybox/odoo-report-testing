import os

try:
    # from odoo 7.0 to 9.0
    from openerp.tests.common import TransactionCase
    from openerp.release import major_version
except:
    # odoo 10.0
    from odoo.tests.common import TransactionCase
    from odoo.release import major_version

from odoo_report_testing.assertions import OdooAssertions


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
        model = 'ir.module.module'
        report = 'ir.module.reference'
        if major_version == '7.0':
            ref_file = 'technical_guide_report_webkit_v7.pdf'
            object_id = self.ref('base.module_report_webkit')
        elif major_version == '8.0':
            object_id = self.env.ref('base.module_report_webkit').id
            ref_file = 'technical_guide_report_webkit_v8.pdf'
        else:  # version 9
            object_id = self.env.ref('base.model_base_language_install').id
            model = 'ir.model'
            ref_file = 'model_base_language_install_v9.pdf'
            report = 'base.report_irmodeloverview'

        ref_file = os.path.join(
            os.path.dirname(__file__), 'demo', ref_file
        )
        self.assertOdooReport(
            ref_file, model, report, [object_id]
        )
