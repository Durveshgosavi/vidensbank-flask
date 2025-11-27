"""
PDF Generation Module for Vidensbank
Generates PDF reports from HTML templates using WeasyPrint
"""

from flask import render_template, make_response
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from datetime import datetime
import io


class PDFGenerator:
    """Handles PDF generation for various report types"""

    def __init__(self):
        self.font_config = FontConfiguration()

    def generate_emissions_report(self):
        """
        Generate a comprehensive PDF report for the Emissions topic

        Returns:
            Flask Response object with PDF content
        """
        # Get current date for the report
        current_date = datetime.now().strftime('%d. %B %Y')

        # Render the HTML template
        html_content = render_template(
            'pdf/emissions_report.html',
            current_date=current_date
        )

        # Generate PDF from HTML
        pdf_file = HTML(string=html_content).write_pdf(
            font_config=self.font_config
        )

        # Create Flask response
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Emissions_Report_{datetime.now().strftime("%Y%m%d")}.pdf'

        return response

    def generate_custom_report(self, template_name, filename, **template_vars):
        """
        Generate a custom PDF report from any template

        Args:
            template_name: Path to the template relative to templates/
            filename: Name for the downloaded PDF file
            **template_vars: Variables to pass to the template

        Returns:
            Flask Response object with PDF content
        """
        # Add current date to template variables
        template_vars['current_date'] = datetime.now().strftime('%d. %B %Y')

        # Render the HTML template
        html_content = render_template(template_name, **template_vars)

        # Generate PDF from HTML
        pdf_file = HTML(string=html_content).write_pdf(
            font_config=self.font_config
        )

        # Create Flask response
        response = make_response(pdf_file)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'

        return response
