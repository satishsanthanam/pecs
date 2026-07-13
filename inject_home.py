#!/usr/bin/env python3
import os
import re

TARGET_DIR = "."
EXCLUDE_DIRS = {'.git', '.github', '.rclone-spool'}

def inject_home_buttons():
    print("🚀 Injecting mobile-adaptive Home buttons across all pages...")
    modified_count = 0

    for root, dirs, files in os.walk(TARGET_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_path = os.path.relpath(root, TARGET_DIR)
        if rel_path == ".":
            continue
            
        depth = len(rel_path.split(os.sep))
        relative_home_link = "../" * depth + "index.html"

        # Responsive layout structure
        home_button_markup = f"""<!-- GLOBAL HOME BUTTON START -->
<style>
    #global-home-button {{
        position: fixed;
        top: 1rem;
        left: 1rem;
        background: #0284c7;
        color: white;
        padding: 0.5rem 1rem;
        text-decoration: none;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        border-radius: 6px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        z-index: 99999;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: background 0.2s, transform 0.2s;
    }}
    #global-home-button:hover {{ background: #0369a1; }}
    
    /* Mobile View Adaptations */
    @media (max-width: 768px) {{
        #global-home-button {{
            top: auto;
            left: auto;
            bottom: 1.5rem;
            right: 1.5rem;
            padding: 0.75rem 1.25rem;
            border-radius: 50px;
            font-size: 0.9rem;
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.3);
        }}
    }}
</style>
<a id="global-home-button" href="{relative_home_link}">
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
    <span>Return to Library</span>
</a>
<!-- GLOBAL HOME BUTTON END -->"""

        for f in files:
            if f.endswith('.html') and f != 'index.html':
                file_path = os.path.join(root, f)
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_data:
                    original_content = file_data.read()

                # 1. Aggressively strip old block AND any surrounding whitespace/creeping newlines
                content_clean = re.sub(
                    r'\s*<!-- GLOBAL HOME BUTTON START -->.*?<!-- GLOBAL HOME BUTTON END -->\s*', 
                    '', 
                    original_content, 
                    flags=re.DOTALL
                )

                # 2. Re-inject the button structure cleanly right after the <body> tag
                body_tag_index = content_clean.find('<body')
                if body_tag_index != -1:
                    closing_bracket_index = content_clean.find('>', body_tag_index)
                    if closing_bracket_index != -1:
                        updated_content = (
                            content_clean[:closing_bracket_index + 1] + 
                            "\n" + home_button_markup + "\n" + 
                            content_clean[closing_bracket_index + 1:]
                        )
                        
                        # 3. 🛡️ IDEMPOTENCY GUARD: Only rewrite if modifications actually occurred
                        if original_content != updated_content:
                            with open(file_path, 'w', encoding='utf-8') as file_data:
                                file_data.write(updated_content)
                            modified_count += 1

    print(f"🏁 Finished! Updated {modified_count} pages with responsive navigation links.")

if __name__ == "__main__":
    inject_home_buttons()
