import os

def patch_html_files():
    print("🧹 Scanning directory for existing clinical files...")
    patched_count = 0

    # Walk through all categories and subcategories recursively
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".html") and file != "index.html" and file != "search.html":
                file_path = os.path.join(root, file)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if the file needs the pagefind tag
                if '<div class="card-body">' in content:
                    updated_content = content.replace(
                        '<div class="card-body">', 
                        '<div class="card-body" data-pagefind-body>'
                    )
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    patched_count += 1

    print(f"🎉 Successful Sweep! Patched {patched_count} existing clinical files with search tags.")

if __name__ == "__main__":
    patch_html_files()
