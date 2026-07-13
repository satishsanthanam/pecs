#!/usr/bin/env python3
import re

def slugify(text):
    text = text.strip()
    text = re.sub(r'[^a-zA-Z0-9]', '-', text).lower()
    return re.sub(r'-+', '-', text).strip('-')

def patch_homepage():
    print("🏗️ Running resilient index.html patch execution...")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Clean previous IDs if present to ensure clean write
    content = re.sub(r'id="cat-[^"]*"', '', content)
    content = re.sub(r'id="sub-[^"]*"', '', content)

    lines = content.splitlines()
    updated_lines = []
    current_cat_slug = ""

    for line in lines:
        cat_match = re.search(r'<summary>📁\s*(.*?)</summary>', line)
        if cat_match:
            cat_name = cat_match.group(1).strip()
            current_cat_slug = slugify(cat_name)
            line = line.replace('<summary>', f'<summary id="cat-{current_cat_slug}">')
        
        sub_match = re.search(r'<summary>📂\s*(.*?)</summary>', line)
        if sub_match:
            sub_name = sub_match.group(1).strip()
            sub_slug = slugify(sub_name)
            line = line.replace('<summary>', f'<summary id="sub-{current_cat_slug}-{sub_slug}">')
            
        updated_lines.append(line)

    patched_content = "\n".join(updated_lines)

    accordion_js = """
<script>
window.addEventListener('DOMContentLoaded', () => {
    const handleHash = () => {
        const hash = window.location.hash;
        if (!hash) return;
        const target = document.querySelector(hash);
        if (target) {
            let parent = target.closest('details');
            while (parent) {
                parent.open = true;
                parent = parent.parentElement.closest('details');
            }
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

    # Clear previous JS script block if it exists to avoid duplication
    patched_content = re.sub(r'<script>.*hashchange.*?</script>\s*</body>', '</body>', patched_content, flags=re.DOTALL)
    
    # Case-insensitive safe injection right before closing body tag
    patched_content = re.sub(r'(</body\s*>)', accordion_js, patched_content, flags=re.IGNORECASE)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(patched_content)
        
    print("🎉 Success! Homepage accordion linkages fully synchronized.")

if __name__ == "__main__":
    patch_homepage()
