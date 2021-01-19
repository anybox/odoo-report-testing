import os
import subprocess
from subprocess import call


class pdftools(object):
    """Utility class to generate pdf file from odoo record, compare
    2 pdf files
    """

    @staticmethod
    def imagediff(ref, compared, output_dir=None):
        """Test if two images are equals, if not, this generate a diff file and
        a animated gif file to highlight differences.

        It can be two single page pdf file.

        This delegate the work to ``compare`` application installed with
        **imagemagick** package which is required.

        :param ref: a ``path`` to the file used as reference, expected result
        :param compared: a ``path`` to the file to compare to the ref file.
        :output_dir: Directory to generate diff files

        return (Boolean equals, [String path to diff files,]): The result is a
        a tuple with bool value to tell if files are equals or not, and a list
        of diff files generated.
        """
        if not os.path.isfile(ref):
            raise RuntimeError("ref file not found %r" % ref)
        if not os.path.isfile(compared):
            raise RuntimeError("Compared file not found %r" % compared)
        result = {
            'reference': ref,
            'compared': compared,
        }
        output_dir, filename = pdftools.outputs_env(
            compared, output_dir=output_dir
        )
        png_output = os.path.join(output_dir, filename + '_diff.png')

        if pdftools.files_equals(ref, compared, png_output):
            result.update(
                {
                    'equal': True,
                    'diff_files': [png_output],
                }
            )
        else:
            gif_output = os.path.join(output_dir, filename + '_diff.gif')
            call([
                'convert', '-delay', '50', ref, compared,
                '-loop', '0', 'animated', gif_output
            ])
            result.update(
                {
                    'equal': False,
                    'diff_files': [png_output, gif_output]
                }
            )
        return result

    @staticmethod
    def files_equals(ref, compared, output):
        equal = False
        p = subprocess.Popen(
            ['compare', '-metric', 'AE', ref, compared, output],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        try:
            p.wait()
            _, err = p.communicate()
            if err.decode('utf-8').strip().split('\n')[-1] == '0':
                equal = True
        except Exception as err:
            p.kill()
            p.wait()
            raise RuntimeError("Something goes wrong while comparing file")
        return equal

    @staticmethod
    def pdfdiff(ref, compared, output_dir=None):
        """Test if two pdf are equals

        This split the pdf and delegate to imagediff to compare each pages.

        To split the pdf ``pdftk`` application from **pdftk** package is
        required.
        """
        if not os.path.isfile(ref):
            raise RuntimeError(
                "ref file not found %r (while comparing with %r)" % (ref, compared)
            )
        if not os.path.isfile(compared):
            raise RuntimeError("Compared file not found %r" % compared)
        output_dir, filename = pdftools.outputs_env(
            compared, output_dir=output_dir
        )
        # split documents
        call([
            'pdftk', ref, 'burst', 'output',
            os.path.join(output_dir, filename + '_ref_page_%02d.pdf')
        ])
        call([
            'pdftk', compared, 'burst', 'output',
            os.path.join(output_dir, filename + '_compared_page_%02d.pdf')
        ])
        ref_pages = pdftools.findPages(output_dir, filename + '_ref_page_')
        compared_pages = pdftools.findPages(
            output_dir, filename + '_compared_page_'
        )
        result = {
            'equal': len(ref_pages) == len(compared_pages),
            'reference': ref,
            'reference_count': len(ref_pages),
            'compared': compared,
            'compared_count': len(compared_pages),
            'pages_compared': 0,
            'pages_equals': 0,
            'pages': []
        }
        for ref_page, compared_page in zip(ref_pages, compared_pages):
            diff = pdftools.imagediff(
                os.path.join(output_dir, ref_page),
                os.path.join(output_dir, compared_page),
                output_dir=output_dir
            )
            result['pages'].append(diff)
            result.update(
                {'pages_compared': result.get('pages_compared', 0) + 1}
            )
            if diff.get('equal'):
                result.update(
                    {'pages_equals': result.get('pages_equals', 0) + 1}
                )
            else:
                result.update({'equal': False})
        return result

    @staticmethod
    def outputs_env(expected_file, output_dir=None):
        """Return tuple with directory and base file name to use from
        expected file
        """
        return (
            output_dir if output_dir else os.getenv(
                'REPORT_TESTING_OUTPUT_DIR', os.path.dirname(expected_file)
            ),
            os.path.splitext(os.path.basename(expected_file))[0]
        )

    @staticmethod
    def findPages(directory, filename_start_width, extension='.pdf'):
        pages = [
            f for f in os.listdir(directory) if
            f.startswith(filename_start_width) and
            f.endswith(extension)
        ]
        pages.sort()
        return pages

    @staticmethod
    def generateReport(
        env, report_service_name, ids, data=None,
    ):
        """Generate the report and return it as a tuple (result, format)
            where `result` is the report document and `format` is the file
            extension.
        """
        report = env['ir.actions.report'].search([("report_name", "=", report_service_name)])
        report.ensure_one() 
        return report.with_context(force_report_rendering=True)._render_qweb_pdf(ids, data=data)