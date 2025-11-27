# PDF Download Implementation Guide

## Overview

This document describes the implementation of PDF report generation for the Vidensbank website, specifically for the Emissions & Sustainability topic.

## Implementation Summary

### 1. Components Created

#### A. PDF Template (`templates/pdf/emissions_report.html`)
A comprehensive, print-optimized HTML template with:
- **Cover Page**: Branded cover with topic title and date
- **Table of Contents**: 7 main sections with page numbers
- **Section 1**: What are Food-Related Emissions? (CO₂e, lifecycle, emission categories)
- **Section 2**: Why is it Important? (Denmark's climate goals, canteen roles)
- **Section 3**: Goals & Ambition (Knowledge to action framework)
- **Section 4**: My Impact (Key levers, everyday decisions)
- **Section 5**: Tips & Tricks (Menu development, purchasing, food waste, communication)
- **Section 6**: Tools & Resources (CO₂ calculator, external links)
- **Section 7**: Summary & Next Steps (Key takeaways, action checklist)

**Design Features**:
- Professional A4 layout optimized for printing
- Green color scheme (#1e5631, #3a7d4c) matching brand
- Infographic elements (lifecycle diagrams, stat cards, emission categories)
- Print-friendly styling with page breaks
- High readability with proper typography hierarchy

#### B. PDF Generator Module (`pdf_generator.py`)
A Python class that handles PDF generation using WeasyPrint:
- `generate_emissions_report()`: Generates the complete emissions PDF
- `generate_custom_report()`: Reusable method for future PDF templates
- Proper font configuration and error handling

#### C. Flask Route (`app.py`)
New route added:
```python
@app.route('/vidensbank/emissioner/download-pdf')
def emissions_download_pdf():
    """Generate and download PDF report for Emissions topic"""
```

#### D. UI Components
**Landing Page Button** (`templates/topics/emissions/landing.html`):
- Prominent download button on the main emissions landing page
- Eye-catching design with icon and description
- Located after the section header for maximum visibility

**CSS Styling** (`static/css/style.css`):
- `.pdf-download-section`: Container with gradient background
- `.pdf-download-button`: Main button with hover effects
- `.pdf-download-compact`: Smaller button for sub-pages (future use)

### 2. Technical Stack

- **WeasyPrint**: HTML to PDF conversion library
- **Flask**: Web framework integration
- **Pillow**: Image processing support
- **FontTools**: Font handling for PDF generation

### 3. Content Structure Analyzed

Based on the existing emissions topic pages:

1. **Landing Page**: Overview and navigation hub
2. **What (Hvad)**: CO₂e definition, food lifecycle (5 phases), emission categories
3. **Why (Hvorfor)**: Denmark's climate goals, canteens as key players, risks vs opportunities
4. **Goal (Mål)**: Knowledge to action framework, canteen ambitions, dialogue tool
5. **Impact (Aftryk)**: 3 key levers (menu, purchasing, food waste), practical examples
6. **Tips**: Menu development, purchasing, waste reduction, operations, guest communication
7. **Tools**: CO₂ calculator access
8. **Cases**: Placeholder for future case studies

## Usage

### For End Users

1. Visit the Emissions topic landing page: `/vidensbank/emissioner`
2. Click the "Download Komplet Guide som PDF" button
3. PDF report will be generated and downloaded automatically
4. Filename format: `Emissions_Report_YYYYMMDD.pdf`

### For Developers

#### Adding PDF to Other Topics

```python
# 1. Create a new template in templates/pdf/
# Example: templates/pdf/nutrition_report.html

# 2. Use the PDF generator in your route
from pdf_generator import PDFGenerator

@app.route('/vidensbank/ernaering/download-pdf')
def nutrition_download_pdf():
    pdf_gen = PDFGenerator()
    return pdf_gen.generate_custom_report(
        template_name='pdf/nutrition_report.html',
        filename='Nutrition_Report.pdf',
        # Add any template variables here
        topic_name='Ernæring',
        sections=['section1', 'section2']
    )
```

#### Customizing the PDF Template

The template uses inline CSS for maximum PDF compatibility. Key areas to customize:

- **Colors**: Update gradient colors in `.section-header`, `.stat-card`, etc.
- **Layout**: Adjust `@page` margins and sizes
- **Page Breaks**: Use `page-break-before: always` or `page-break-inside: avoid`
- **Infographics**: Modify `.lifecycle-container`, `.emission-categories`, `.stats-grid`

## Benefits

### For Users
- **Offline Access**: Download and read without internet
- **Sharing**: Easy to share with colleagues via email
- **Printing**: Print-optimized for physical distribution
- **Comprehensive**: All content in one structured document
- **Professional**: High-quality design suitable for presentations

### For Business
- **Lead Generation**: Track downloads as engagement metric
- **Brand Authority**: Professional documents build credibility
- **Content Reuse**: PDFs can be used in marketing materials
- **Accessibility**: Multiple format options for different preferences

## Future Enhancements

### Short-term
1. Add compact PDF download buttons to sub-pages (what, why, goal, etc.)
2. Add download tracking/analytics
3. Create PDF templates for other topics (Ernæring, Madspild, etc.)
4. Add option to include/exclude specific sections

### Long-term
1. Personalized PDFs with user data from climate calculator
2. Dynamic infographics based on canteen-specific data
3. Multi-language support (English, German)
4. Interactive PDF with fillable checklists
5. Email delivery option
6. Integration with CRM for follow-up

## Testing Checklist

- [x] Python syntax validation (app.py, pdf_generator.py)
- [x] CSS styling added and properly formatted
- [x] Landing page button integration
- [ ] Test PDF generation in development environment
- [ ] Verify PDF renders correctly in multiple PDF readers
- [ ] Test on mobile devices (responsive button)
- [ ] Test download on different browsers
- [ ] Verify all infographics render correctly
- [ ] Check page breaks and layout
- [ ] Test error handling (missing template, etc.)

## Deployment Notes

### Prerequisites
```bash
pip install weasyprint
```

### Environment Variables
No additional environment variables required.

### Assets
Ensure static CSS files are accessible:
- `/static/css/style.css` - Contains PDF button styles

### Production Considerations
1. **Performance**: PDF generation can be CPU-intensive. Consider:
   - Caching generated PDFs for 24 hours
   - Using a background task queue for large reports
   - Rate limiting to prevent abuse

2. **Security**:
   - Validate all input parameters
   - Sanitize any user-provided content before PDF generation
   - Set appropriate content-disposition headers

3. **Monitoring**:
   - Log PDF generation requests
   - Track success/failure rates
   - Monitor generation time

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'weasyprint'`
- **Solution**: Install WeasyPrint: `pip install weasyprint`

**Issue**: PDF generation fails with font errors
- **Solution**: WeasyPrint automatically downloads fonts. Ensure internet connection or install fonts locally.

**Issue**: Images not rendering in PDF
- **Solution**: Use absolute URLs for images or base64 encode them

**Issue**: Page breaks in wrong places
- **Solution**: Add `page-break-inside: avoid` to container elements

## Credits

- **Design Inspiration**: Awwwards-style UI/UX
- **Content Source**: Existing emissions topic pages in Vidensbank
- **PDF Generation**: WeasyPrint library
- **Icons**: Inline SVG for compatibility

## Contact

For questions or issues related to PDF generation, contact the development team.

---

**Last Updated**: November 27, 2025
**Version**: 1.0.0
