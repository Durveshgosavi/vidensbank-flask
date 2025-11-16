import glob
import re

# Process all product HTML files
for filepath in glob.glob('templates/products/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all Unsplash URLs in hero sections and add quality parameters
    # Pattern: url('https://images.unsplash.com/photo-XXXXX')
    def enhance_unsplash_url(match):
        url = match.group(1)
        # Remove any existing parameters
        base_url = url.split('?')[0]
        # Add premium quality parameters
        enhanced_url = f"{base_url}?w=1920&q=85&fit=crop&crop=entropy"
        return f"url('{enhanced_url}')"

    # Replace Unsplash URLs in background-image styles
    content = re.sub(
        r"url\('(https://images\.unsplash\.com/photo-[^']+)'\)",
        enhance_unsplash_url,
        content
    )

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Enhanced hero in {filepath}")

print("\n✅ All hero sections enhanced with premium image quality!")
