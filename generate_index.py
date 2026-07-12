#!/usr/bin/env python3
import os
import urllib.parse

# Configuration
TARGET_DIR = "."
OUTPUT_FILE = "index.html"
EXCLUDE_DIRS = {'.git', '.github', '.rclone-spool'}
EXCLUDE_FILES = {'index.html', 'build_index.py', 'patient_education.xlsx', 'server.log'}

def generate_index():
    print("📂 Scanning directories and building streamlined hyperlink tree...")
    tree = {}
    
    for root, dirs, files in os.walk(TARGET_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_path = os.path.relpath(root, TARGET_DIR)
        if rel_path == ".":
            continue
            
        parts = rel_path.split(os.sep)
        if len(parts) >= 2:
            category = parts[0]
            subcategory = parts[1]
            
            topic_files = {}
            for f in files:
                if f in EXCLUDE_FILES or f.startswith('.'):
                    continue
                
                base_name, ext = os.path.splitext(f)
                # We only track HTML files for the UI display now
                if ext.lower() == '.html':
                    full_rel_path = os.path.join(rel_path, f)
                    safe_url = urllib.parse.quote(full_rel_path)
                    topic_files[base_name] = safe_url

            if topic_files:
                if category not in tree:
                    tree[category] = {}
                if subcategory not in tree[category]:
                    tree[category][subcategory] = []
                
                for topic, url in topic_files.items():
                    display_name = topic.replace('_', ' ').replace('-', ' ').title()
                    tree[category][subcategory].append((display_name, url))

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Reference Library</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { --primary: #0284c7; --text: #0f172a; --bg: #f8fafc; --card-bg: #ffffff; --border: #e2e8f0; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg); color: var(--text); padding: 2rem 1rem; line-height: 1.5; }
        .container { max-width: 900px; margin: 0 auto; }
        header { margin-bottom: 2rem; text-align: left; border-bottom: 1px solid var(--border); padding-bottom: 1.5rem; }
        h1 { font-size: 2rem; font-weight: 700; color: #1e293b; letter-spacing: -0.02em; }
        p.subtitle { color: #64748b; font-size: 0.95rem; margin-top: 0.25rem; }
        
        .search-container { position: sticky; top: 1rem; z-index: 100; margin-bottom: 2rem; }
        #searchBar { width: 100%; padding: 0.85rem 1.25rem; font-size: 1rem; border: 1px solid #cbd5e1; border-radius: 8px; background: white; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05); outline: none; }
        #searchBar:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15); }
        
        details { background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 0.75rem; }
        summary { padding: 0.85rem 1.25rem; font-weight: 600; font-size: 1.05rem; color: #1e293b; cursor: pointer; user-select: none; display: flex; align-items: center; justify-content: space-between; list-style: none; }
        summary::-webkit-details-marker { display: none; }
        summary::after { content: ""; width: 6px; height: 6px; border-right: 2px solid #64748b; border-bottom: 2px solid #64748b; transform: rotate(-45deg); transition: transform 0.2s ease; margin-right: 0.25rem; }
        details[open] > summary::after { transform: rotate(45deg); }
        
        .category-content { padding: 0.5rem 1.25rem 1.25rem 1.25rem; border-top: 1px solid #f1f5f9; }
        details.subcategory { border: 1px solid #e2e8f0; background: #fafafa; margin-top: 0.5rem; }
        details.subcategory summary { font-size: 0.95rem; font-weight: 500; color: #475569; padding: 0.65rem 1rem; }
        .subcategory-content { padding: 0.5rem 1rem 1rem 1rem; border-top: 1px solid #e2e8f0; background: #ffffff; }
        
        /* Clean Link Rows */
        .topic-list { list-style: none; padding: 0; margin: 0; }
        .topic-item { margin-bottom: 0.25rem; }
        .topic-link { display: block; text-decoration: none; font-size: 0.92rem; font-weight: 400; color: #334155; padding: 0.5rem 0.75rem; border-radius: 6px; transition: all 0.1s; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .topic-link:hover { background: #e0f2fe; color: #0369a1; padding-left: 1rem; }
        
        .hidden { display: none !important; }
        .no-results { text-align: center; padding: 3rem; color: #94a3b8; font-size: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Clinical Reference Library</h1>
            <p class="subtitle">System Resource Index & Documentation Database</p>
        </header>

        <div class="search-container">
            <input type="text" id="searchBar" placeholder="🔍 Type to filter folders and topics instantly..." onkeyup="filterLibrary()">
        </div>

        <div id="libraryRoot">
"""

    for cat, subcats in sorted(tree.items()):
        html_content += f'\t\t<details class="category" data-node="category">\n'
        html_content += f'\t\t\t<summary>📁 {cat}</summary>\n'
        html_content += f'\t\t\t<div class="category-content">\n'
        
        for subcat, topics in sorted(subcats.items()):
            html_content += f'\t\t\t\t<details class="subcategory" data-node="subcategory">\n'
            html_content += f'\t\t\t\t\t<summary>📂 {subcat}</summary>\n'
            html_content += f'\t\t\t\t\t<div class="subcategory-content">\n'
            html_content += f'\t\t\t\t\t\t<ul class="topic-list">\n'
            
            for topic_name, html_url in sorted(topics):
                html_content += f'\t\t\t\t\t\t\t<li class="topic-item" data-node="topic">\n'
                html_content += f'\t\t\t\t\t\t\t\t<a class="topic-link" href="{html_url}" title="{topic_name}">{topic_name}</a>\n'
                html_content += f'\t\t\t\t\t\t\t</li>\n'
                
            html_content += f'\t\t\t\t\t\t</ul>\n'
            html_content += f'\t\t\t\t\t</div>\n'
            # (Fix: Closing tag for subcategory details was missing here)
            html_content += f'\t\t\t\t</details>\n'
            
        html_content += f'\t\t\t</div>\n'
        html_content += f'\t\t</details>\n'

    html_content += """        </div>
        <div id="noResults" class="no-results hidden">No matching clinical topics found.</div>
    </div>

    <script>
        function filterLibrary() {
            const query = document.getElementById('searchBar').value.toLowerCase().trim();
            const categories = document.querySelectorAll('[data-node="category"]');
            const noResultsMessage = document.getElementById('noResults');
            let totalVisibleTopics = 0;

            categories.forEach(category => {
                let visibleSubcategoriesWithinCategory = 0;
                const subcategories = category.querySelectorAll('[data-node="subcategory"]');

                subcategories.forEach(sub => {
                    let visibleTopicsWithinSub = 0;
                    const topics = sub.querySelectorAll('[data-node="topic"]');

                    topics.forEach(topic => {
                        const text = topic.querySelector('.topic-link').textContent.toLowerCase();
                        if (text.includes(query)) {
                            topic.classList.remove('hidden');
                            visibleTopicsWithinSub++;
                            totalVisibleTopics++;
                        } else {
                            topic.classList.add('hidden');
                        }
                    });

                    if (visibleTopicsWithinSub > 0) {
                        sub.classList.remove('hidden');
                        if (query !== "") sub.setAttribute('open', 'true');
                    } else {
                        sub.classList.add('hidden');
                        if (query === "") sub.removeAttribute('open');
                    }
                });

                if (visibleSubcategoriesWithinCategory > 0) {
                    category.classList.remove('hidden');
                    if (query !== "") category.setAttribute('open', 'true');
                } else {
                    category.classList.add('hidden');
                    if (query === "") category.removeAttribute('open');
                }
            });

            if (totalVisibleTopics === 0 && query !== "") {
                noResultsMessage.classList.remove('hidden');
            } else {
                noResultsMessage.classList.add('hidden');
            }
        }
    </script>
</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"🏁 Success! Hyperlink index generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_index()
