#!/usr/bin/env python3
import os
import re

TARGET_DIR = "."
EXCLUDE_DIRS = {'.git', '.github', '.rclone-spool'}

def slugify(text):
    text = text.strip()
    text = re.sub(r'[^a-zA-Z0-9]', '-', text).lower()
    return re.sub(r'-+', '-', text).strip('-')

def make_badges_clickable_synchronized():
    print("🚀 Syncing vertical header badges with click override enforcement...")
    modified_count = 0

    for root, dirs, files in os.walk(TARGET_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_path = os.path.relpath(root, TARGET_DIR)
        if rel_path == ".":
            continue
            
        parts = rel_path.split(os.sep)
        if len(parts) >= 2:
            category = parts[0]
            subcategory = parts[1]
            
            cat_slug = slugify(category)
            sub_slug = slugify(subcategory)
            
            cat_hash = f"cat-{cat_slug}"
            sub_hash = f"sub-{cat_slug}-{sub_slug}"

            for f in files:
                if f.endswith('.html') and f not in ['index.html', 'search.html']:
                    file_path = os.path.join(root, f)
                    
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_data:
                        content = file_data.read()

                    # Clean out previous <a> setups to rewrite cleanly
                    content_clean = re.sub(r'(<span class=["\']meta-value["\']>)(<a href=".*?">)(.*?)(</a>)(</span>)', r'\1\3\5', content)

                    depth = len(rel_path.split(os.sep))
                    relative_base = "../" * depth

                    updated_content = content_clean
                    is_modified = False

                    # Styled with absolute pointer-events and z-index priority
                    link_style = "text-decoration: none; color: #0f172a; position: relative; z-index: 100; pointer-events: auto; display: inline-block;"

                    # 1. Update Category Badge
                    cat_pattern = r'(<div class=["\']meta-item category-badge["\'].*?<span class=["\']meta-value["\']>)(.*?)(</span></div>)'
                    cat_match = re.search(cat_pattern, updated_content, re.DOTALL)
                    if cat_match:
                        prefix, text, suffix = cat_match.groups()
                        new_html = f'{prefix}<a href="{relative_base}index.html#{cat_hash}" style="{link_style}">{text}</a>{suffix}'
                        updated_content = updated_content.replace(cat_match.group(0), new_html)
                        is_modified = True

                    # 2. Update Subcategory Badge
                    sub_pattern = r'(<div class=["\']meta-item subcategory-badge["\'].*?<span class=["\']meta-value["\']>)(.*?)(</span></div>)'
                    sub_match = re.search(sub_pattern, updated_content, re.DOTALL)
                    if sub_match:
                        prefix, text, suffix = sub_match.groups()
                        new_html = f'{prefix}<a href="{relative_base}index.html#{sub_hash}" style="{link_style}">{text}</a>{suffix}'
                        updated_content = updated_content.replace(sub_match.group(0), new_html)
                        is_modified = True

                    if is_modified and content != updated_content:
                        with open(file_path, 'w', encoding='utf-8') as file_data:
                            file_data.write(updated_content)
                        modified_count += 1

    print(f"🎉 Complete! Injected secure links across {modified_count} files.")

if __name__ == "__main__":
    make_badges_clickable_synchronized()
