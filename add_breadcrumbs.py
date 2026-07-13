import os
import re

def update_existing_files():
    total_updated = 0
    
    # Walk through your project structure
    for root, dirs, files in os.walk('.'):
        # Ignore hidden system or git/vercel directories
        if any(part.startswith('.') for part in root.split(os.sep)):
            continue
            
        parts = root.split(os.sep)
        
        # Structure check: ['.', 'Category', 'Subcategory', 'Topic']
        if len(parts) >= 4:
            category = parts[1]
            subcategory = parts[2]
            
            for file in files:
                if file.endswith('.html') and file not in ['index.html', 'search.html']:
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Skip if breadcrumbs are already injected to prevent duplicates
                    if 'class="clinical-breadcrumbs"' in content:
                        continue
                    
                    # 1. Add the breadcrumb block text
                    breadcrumbs = f'''<!-- 🧭 Elegant Clinical Breadcrumb Navigation -->
    <nav class="clinical-breadcrumbs" style="padding: 0.5rem 0; margin-bottom: 1.5rem; font-size: 0.85rem; color: #64748b; border-bottom: 1px dashed #e2e8f0; font-family: sans-serif;">
      <a href="/index.html" style="color: #2563eb; text-decoration: none; font-weight: 500;">🏠 Home</a>
      <span style="margin: 0 0.4rem; color: #cbd5e1;">/</span>
      <span style="font-weight: 600; color: #334155;">{category}</span>
      <span style="margin: 0 0.4rem; color: #cbd5e1;">/</span>
      <span style="color: #64748b;">{subcategory}</span>
    </nav>'''
                    
                    # Inject breadcrumbs directly right after the opening <body> tag
                    updated = re.sub(r'(<body>)', r'\1\n' + breadcrumbs, content, flags=re.IGNORECASE)
                    
                    # 2. Fix the html lang warning for Pagefind
                    updated = re.sub(r'<html>', '<html lang="en">', updated, flags=re.IGNORECASE)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated)
                        
                    total_updated += 1
                    print(f"✅ Injected breadcrumbs into: {category} -> {subcategory} -> {file}")

    print(f"\n🎉 Done! Successfully updated {total_updated} clinical files.")

if __name__ == "__main__":
    update_existing_files()
