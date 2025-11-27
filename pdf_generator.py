"""
PDF Generation Module for Vidensbank
Generates PDF reports from HTML templates using WeasyPrint
"""

from flask import render_template, make_response
from datetime import datetime
import io
import logging

# Configure logging
logger = logging.getLogger(__name__)

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    # OSError can happen if system dependencies (like Pango/Cairo) are missing
    logger.warning(f"WeasyPrint not available: {e}")
    WEASYPRINT_AVAILABLE = False


class PDFGenerator:
    """Handles PDF generation for various report types"""

    def __init__(self):
        if WEASYPRINT_AVAILABLE:
            try:
                self.font_config = FontConfiguration()
            except Exception as e:
                logger.error(f"Failed to initialize FontConfiguration: {e}")
                self.font_config = None
        else:
            self.font_config = None

        """
        Generate a comprehensive PDF report for the Emissions topic

        Returns:
            Flask Response object with PDF content
        """
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint is not available on this system.")

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
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint is not available on this system.")

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
