#!/usr/bin/env python3
"""
Power Pages to Flask Template Converter
This script helps convert Power Pages HTML exports to Flask templates
"""

import os
import sys
from pathlib import Path

def convert_html_to_flask_template(input_file, output_file):
    """Convert a Power Pages HTML file to a Flask template"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create Flask template structure
    template = f'''{% extends "base.html" %}}

{{% block title %}}TITLE_HERE - Vidensbank{{% endblock %}}

{{% block content %}}
{content}
{{% endblock %}}
'''
    
    # Replace common Power Pages patterns
    # Replace absolute URLs with Flask url_for()
    template = template.replace('/EmissionerogbÃ¦redygtighed/', "{{ url_for('emissions_sustainability') }}")
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"✅ Converted: {input_file} -> {output_file}")

def main():
    """Main conversion function"""
    
    print("=" * 70)
    print("Power Pages to Flask Template Converter")
    print("=" * 70)
    print()
    
    # Get source directory
    if len(sys.argv) > 1:
        source_dir = sys.argv[1]
    else:
        source_dir = input("Enter path to Power Pages web-pages folder: ")
    
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ Error: Directory not found: {source_dir}")
        return
    
    # Get output directory
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # Find all HTML files
    html_files = list(source_path.rglob("*.webpage.copy"))
    
    if not html_files:
        print("❌ No .webpage.copy files found!")
        return
    
    print(f"Found {len(html_files)} HTML files to convert\n")
    
    # Convert each file
    for html_file in html_files:
        # Generate output filename
        output_name = html_file.stem.replace('.webpage.copy', '') + '.html'
        output_name = output_name.lower().replace('-', '_')
        output_file = templates_dir / output_name
        
        try:
            convert_html_to_flask_template(html_file, output_file)
        except Exception as e:
            print(f"❌ Error converting {html_file}: {e}")
    
    print()
    print("=" * 70)
    print("Conversion Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review the converted templates in the 'templates' folder")
    print("2. Update the TITLE_HERE placeholders")
    print("3. Add routes in app.py for each new template")
    print("4. Test your pages locally")

if __name__ == "__main__":
    main()
