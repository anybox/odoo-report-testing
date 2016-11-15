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
from odoo_report_testing.reports import pdftools


class TestReports(TransactionCase, OdooAssertions):

    @classmethod
    def setUpClass(cls):
        super(TestReports, cls).setUpClass()
        cls.maxDiff = None

    def test_getOutputDir(self):
        save_env = os.getenv('REPORT_TESTING_OUTPUT_DIR', False)
        os.environ.get('REPORT_TESTING_OUTPUT_DIR')
        file = '/tmp/test/file.rst'
        self.assertEqual(
            ('/tmp', 'file'),
            pdftools.outputs_env(file, output_dir='/tmp')
        )
        self.assertEqual(('/tmp/test', 'file'), pdftools.outputs_env(file))
        os.environ.update({'REPORT_TESTING_OUTPUT_DIR': '/tmp/other'})
        self.assertEqual(
            ('/tmp', 'file'),
            pdftools.outputs_env(file, output_dir='/tmp')
        )
        self.assertEqual(('/tmp/other', 'file'), pdftools.outputs_env(file))
        if save_env:
            os.environ.update({'REPORT_TESTING_OUTPUT_DIR': save_env})

    def test_imagediff(self):
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_01.pdf'
        )
        file2 = file1
        diff = pdftools.imagediff
        output_files = ['/tmp/single_page_01_diff.png']
        self.assertEquals(
            {
                'equal': True,
                'reference': file1,
                'compared': file2,
                'diff_files': output_files,
            },
            diff(file1, file2, output_dir='/tmp/')
        )
        for f in output_files:
            self.assertTrue(os.path.isfile(f))
            os.remove(f)
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_00.pdf'
        )
        output_files.append('/tmp/single_page_01_diff.gif')
        self.assertEquals(
            {
                'equal': False,
                'reference': file1,
                'compared': file2,
                'diff_files': output_files,
            },
            diff(file1, file2, output_dir='/tmp/')
        )
        for f in output_files:
            self.assertTrue(os.path.isfile(f))
            os.remove(f)
        file2 = 'NonExistsFile'
        self.assertRaises(RuntimeError, diff, file1, file2)
        file1 = 'NonExistsFile'
        self.assertRaises(RuntimeError, diff, file1, file2)
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_01.pdf'
        )
        self.assertRaises(RuntimeError, diff, file1, file2)

    def test_pdfdiff_errors(self):
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        diff = pdftools.pdfdiff
        file2 = 'NonExistsFile'
        self.assertRaises(RuntimeError, diff, file1, file2)
        file1 = 'NonExistsFile'
        self.assertRaises(RuntimeError, diff, file1, file2)
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'single_page_01.pdf'
        )
        self.assertRaises(RuntimeError, diff, file1, file2)

    def test_pdfdiff_equal(self):
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        file2 = file1
        diff = pdftools.pdfdiff
        values = {
            'equal': True,
            'reference': file1,
            'reference_count': 4,
            'compared': file2,
            'compared_count': 4,
            'pages_compared': 4,
            'pages_equals': 4,
            'pages': [
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_ref_ref_page_01.pdf',
                    'compared': '/tmp/multi_page_ref_compared_page_01.pdf',
                    'diff_files': [
                        '/tmp/multi_page_ref_compared_page_01_diff.png',
                    ],
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_ref_ref_page_02.pdf',
                    'compared': '/tmp/multi_page_ref_compared_page_02.pdf',
                    'diff_files': [
                        '/tmp/multi_page_ref_compared_page_02_diff.png',
                    ],
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_ref_ref_page_03.pdf',
                    'compared': '/tmp/multi_page_ref_compared_page_03.pdf',
                    'diff_files': [
                        '/tmp/multi_page_ref_compared_page_03_diff.png',
                    ],
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_ref_ref_page_04.pdf',
                    'compared': '/tmp/multi_page_ref_compared_page_04.pdf',
                    'diff_files': [
                        '/tmp/multi_page_ref_compared_page_04_diff.png',
                    ],
                },
            ]
        }
        self.assertEqual(values, diff(file1, file2, output_dir='/tmp/'))
        self.clean(values)

    def test_pdfdiff_one_page_diff(self):
        diff = pdftools.pdfdiff
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_diff_p2.pdf'
        )
        values = {
            'equal': False,
            'reference': file1,
            'reference_count': 4,
            'compared': file2,
            'compared_count': 4,
            'pages_compared': 4,
            'pages_equals': 3,
            'pages': [
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_p2_ref_page_01.pdf',
                    'compared': '/tmp/multi_page_diff_p2_compared_page_01.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2_compared_page_01_diff.png',
                    ],
                },
                {
                    'equal': False,
                    'reference': '/tmp/multi_page_diff_p2_ref_page_02.pdf',
                    'compared': '/tmp/multi_page_diff_p2_compared_page_02.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2_compared_page_02_diff.png',
                        '/tmp/multi_page_diff_p2_compared_page_02_diff.gif',
                    ],
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_p2_ref_page_03.pdf',
                    'compared': '/tmp/multi_page_diff_p2_compared_page_03.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2_compared_page_03_diff.png'],
                    },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_p2_ref_page_04.pdf',
                    'compared': '/tmp/multi_page_diff_p2_compared_page_04.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2_compared_page_04_diff.png'],
                    },
            ]
        }
        self.assertEqual(values, diff(file1, file2, output_dir='/tmp/'))
        self.clean(values)

    def test_pdfdiff_two_pages_diff(self):
        diff = pdftools.pdfdiff
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_diff_p2-p3.pdf'
        )
        values = {
            'equal': False,
            'reference': file1,
            'reference_count': 4,
            'compared': file2,
            'compared_count': 4,
            'pages_compared': 4,
            'pages_equals': 2,
            'pages': [
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_p2-p3_ref_page_01.pdf',
                    'compared':
                        '/tmp/multi_page_diff_p2-p3_compared_page_01.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2-p3_compared_page_01_diff.png'
                    ],
                },
                {
                    'equal': False,
                    'reference': '/tmp/multi_page_diff_p2-p3_ref_page_02.pdf',
                    'compared':
                        '/tmp/multi_page_diff_p2-p3_compared_page_02.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2-p3_compared_page_02_diff.png',
                        '/tmp/multi_page_diff_p2-p3_compared_page_02_diff.gif',
                    ],
                },
                {
                    'equal': False,
                    'reference': '/tmp/multi_page_diff_p2-p3_ref_page_03.pdf',
                    'compared':
                        '/tmp/multi_page_diff_p2-p3_compared_page_03.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2-p3_compared_page_03_diff.png',
                        '/tmp/multi_page_diff_p2-p3_compared_page_03_diff.gif'
                    ],
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_p2-p3_ref_page_04.pdf',
                    'compared':
                        '/tmp/multi_page_diff_p2-p3_compared_page_04.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_p2-p3_compared_page_04_diff.png'
                    ],
                },
            ]
        }
        self.assertEqual(values, diff(file1, file2, output_dir='/tmp/'))
        self.clean(values)

    def test_pdfdiff_pages_diff(self):
        diff = pdftools.pdfdiff
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_diff_pages.pdf'
        )
        values = {
            'equal': False,
            'reference': file1,
            'reference_count': 4,
            'compared': file2,
            'compared_count': 3,
            'pages_compared': 3,
            'pages_equals': 3,
            'pages': [
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_pages_ref_page_01.pdf',
                    'compared':
                        '/tmp/multi_page_diff_pages_compared_page_01.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_pages_compared_page_01_diff.png'
                    ],
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_pages_ref_page_02.pdf',
                    'compared':
                        '/tmp/multi_page_diff_pages_compared_page_02.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_pages_compared_page_02_diff.png'
                    ]
                },
                {
                    'equal': True,
                    'reference': '/tmp/multi_page_diff_pages_ref_page_03.pdf',
                    'compared':
                        '/tmp/multi_page_diff_pages_compared_page_03.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_pages_compared_page_03_diff.png',
                    ]
                },
            ]
        }
        self.assertEqual(values, diff(file1, file2, output_dir='/tmp/'))
        self.clean(values)

    def test_pdfdiff_pages_diff_p2(self):
        diff = pdftools.pdfdiff
        file1 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_ref.pdf'
        )
        file2 = os.path.join(
            os.path.dirname(__file__), 'demo', 'multi_page_diff_pages-p2.pdf'
        )
        values = {
            'equal': False,
            'reference': file1,
            'reference_count': 4,
            'compared': file2,
            'compared_count': 3,
            'pages_compared': 3,
            'pages_equals': 2,
            'pages': [
                {
                    'equal': True,
                    'reference':
                        '/tmp/multi_page_diff_pages-p2_ref_page_01.pdf',
                    'compared':
                        '/tmp/multi_page_diff_pages-p2_compared_page_01.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_pages-p2'
                        '_compared_page_01_diff.png'
                    ],
                },
                {
                    'equal': False,
                    'reference':
                        '/tmp/multi_page_diff_pages-p2_ref_page_02.pdf',
                    'compared':
                        '/tmp/multi_page_diff_pages-p2_compared_page_02.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_pages-p2_'
                        'compared_page_02_diff.png',
                        '/tmp/multi_page_diff_pages-p2_'
                        'compared_page_02_diff.gif',
                    ]
                },
                {
                    'equal': True,
                    'reference':
                        '/tmp/multi_page_diff_pages-p2_ref_page_03.pdf',
                    'compared':
                        '/tmp/multi_page_diff_pages-p2_compared_page_03.pdf',
                    'diff_files': [
                        '/tmp/multi_page_diff_pages-p2_'
                        'compared_page_03_diff.png',
                    ]
                },
            ]
        }
        self.assertEqual(values, diff(file1, file2, output_dir='/tmp/'))
        self.clean(values)

    def test_generate_report(self):
        version7 = False
        model = 'ir.module.module'
        report = 'ir.module.reference'
        if major_version == '7.0':
            version7 = True
            object_id = self.ref('base.module_report_webkit')
        elif major_version == '8.0':
            object_id = self.env.ref('base.module_report_webkit').id
        else:  # version 9
            object_id = self.env.ref('base.model_base_language_install').id
            model = 'ir.model'
            report = 'base.report_irmodeloverview'
        pdftools.generateReport(
            self.cr, self.uid, model, report, [object_id], version7=version7
        )

    def clean(self, values):
        for page in values.get('pages'):
            os.remove(page.get('reference'))
            os.remove(page.get('compared'))
            for f in page.get('diff_files'):
                os.remove(f)
