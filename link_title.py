#!/usr/bin/env python3
import re

def link_main_title():
    print("🔗 Hyperlinking 'Clinical Reference Library' title text...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Idempotency check: Skip if already hyperlinked to index.html
    if 'href="index.html"' in content and 'Clinical Reference Library' in content:
        if re.search(r'href=["\']index\.html["\'][^>]*>Clinical Reference Library', content):
            print("⚠️ The homepage title is already hyperlinked!")
            return

    # Targeting the text inside <h1> or standard text blocks flexibly
    target_pattern = r'(<h1>\s*)(Clinical Reference Library)(\s*</h1>)'
    match = re.search(target_pattern, content)
    
    if match:
        prefix, text, suffix = match.groups()
        new_html = f'{prefix}<a href="index.html" style="text-decoration: none; color: inherit; transition: opacity 0.2s;">{text}</a>{suffix}'
        updated_content = content.replace(match.group(0), new_html)
    else:
        # Fallback loose replacement if it lives inside an h2 or alternative wrapper
        updated_content = re.sub(
            r'(?<!["\'>])Clinical Reference Library(?!</a>)',
            '<a href="index.html" style="text-decoration: none; color: inherit;">Clinical Reference Library</a>',
            content
        )

    if content != updated_content:
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("🎉 Success! Main branding header is now fully interactive.")
    else:
        print("❌ Could not locate the exact 'Clinical Reference Library' text block to patch.")

if __name__ == "__main__":
    link_main_title()
