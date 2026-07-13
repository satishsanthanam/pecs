#!/usr/bin/env python3
import os
import re

TARGET_DIR = "."
EXCLUDE_DIRS = {'.git', '.github', '.rclone-spool'}

def remove_old_breadcrumbs():
    print("🧹 Cleaning up old horizontal breadcrumb blocks...")
    modified_count = 0

    for root, dirs, files in os.walk(TARGET_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for f in files:
            if f.endswith('.html') and f not in ['index.html', 'search.html']:
                file_path = os.path.join(root, f)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_data:
                    content = file_data.read()

                # Check if the old navigation block exists
                if 'class="clinical-breadcrumbs"' in content or '<!-- 🧭 Elegant Clinical Breadcrumb Navigation' in content:
                    # Match the comment and the nav block aggressively including surrounding whitespace
                    cleaned_content = re.sub(
                        r'\s*<!-- 🧭 Elegant Clinical Breadcrumb Navigation.*?-->\s*<nav class="clinical-breadcrumbs".*?</nav>\s*',
                        '\n',
                        content,
                        flags=re.DOTALL
                    )
                    
                    # Backup fallback in case the comment wasn't there
                    cleaned_content = re.sub(
                        r'\s*<nav class="clinical-breadcrumbs".*?</nav>\s*',
                        '\n',
                        cleaned_content,
                        flags=re.DOTALL
                    )

                    if content != cleaned_content:
                        with open(file_path, 'w', encoding='utf-8') as file_data:
                            file_data.write(cleaned_content)
                        modified_count += 1
                        print(f"🧹 Stripped horizontal bar from: {f}")

    print(f"\n🎉 Success! Cleaned up {modified_count} files. Your vertical layout is now pristine.")

if __name__ == "__main__":
    remove_old_breadcrumbs()
