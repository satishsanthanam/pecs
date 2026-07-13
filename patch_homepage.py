#!/usr/bin/env python3
import re

def slugify(text):
    text = text.strip()
    text = re.sub(r'[^a-zA-Z0-9]', '-', text).lower()
    return re.sub(r'-+', '-', text).strip('-')

def patch_homepage():
    print("🏗️ Patching index.html with accordion IDs and deep-linking expansion rules...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Avoid double patching
    if 'id="cat-' in content:
        print("⚠️ index.html appears to already be patched with IDs.")
        return

    lines = content.splitlines()
    updated_lines = []
    current_cat_slug = ""

    for line in lines:
        # 1. Catch Category Summaries
        cat_match = re.search(r'<summary>📁\s*(.*?)</summary>', line)
        if cat_match:
            cat_name = cat_match.group(1).strip()
            current_cat_slug = slugify(cat_name)
            line = line.replace('<summary>', f'<summary id="cat-{current_cat_slug}">')
        
        # 2. Catch Subcategory Summaries
        sub_match = re.search(r'<summary>📂\s*(.*?)</summary>', line)
        if sub_match:
            sub_name = sub_match.group(1).strip()
            sub_slug = slugify(sub_name)
            # Combined slug to prevent duplicate name collisions across categories
            line = line.replace('<summary>', f'<summary id="sub-{current_cat_slug}-{sub_slug}">')
            
        updated_lines.append(line)

    patched_content = "\n".join(updated_lines)

    # 3. Inject the clean Accordion Auto-Expander JS right before the closing body tag
    accordion_js = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const handleHash = () => {
        const hash = window.location.hash;
        if (!hash) return;
        const target = document.querySelector(hash);
        if (target) {
            // Traverse upwards and automatically expand all collapsed parent details accordions
            let parent = target.closest('details');
            while (parent) {
                parent.open = true;
                parent = parent.parentElement.closest('details');
            }
            // Smoothly center the element on the screen
            setTimeout(() => {
                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 150);
        }
    };
    handleHash();
    window.addEventListener('hashchange', handleHash);
});
</script>
</body>"""

    if 'window.addEventListener(\'hashchange\'' not in patched_content:
        patched_content = patched_content.replace('</body>', accordion_js)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(patched_content)
        
    print("🎉 Success! index.html is now optimized for deep-linking navigation.")

if __name__ == "__main__":
    patch_homepage()
