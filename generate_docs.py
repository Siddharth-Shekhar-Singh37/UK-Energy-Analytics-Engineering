import json
import os

def generate_static_docs():
    # 1. Path to your dbt artifacts
    target_path = 'target'
    output_path = 'docs/index.html'
    
    # 2. Load the essential dbt files
    with open(os.path.join(target_path, 'index.html'), 'r') as f:
        content = f.read()

    with open(os.path.join(target_path, 'manifest.json'), 'r') as f:
        manifest = json.load(f)

    with open(os.path.join(target_path, 'catalog.json'), 'r') as f:
        catalog = json.load(f)

    # 3. "Stitch" the JSON files into the HTML file
    content = content.replace('report_type: "regular"', 'report_type: "static"')
    
    # Inject manifest
    manifest_string = json.dumps(manifest).replace('"', '\\"')
    content = content.replace('var o = {manifest: "REPLACE_ME_MANIFEST", catalog: "REPLACE_ME_CATALOG"};', 
                              f'var o = {{manifest: "{manifest_string}", catalog: "REPLACE_ME_CATALOG"}};')
    
    # Inject catalog
    catalog_string = json.dumps(catalog).replace('"', '\\"')
    content = content.replace('catalog: "REPLACE_ME_CATALOG"', f'catalog: "{catalog_string}"')

    # 4. Save the single file to the docs folder
    if not os.path.exists('docs'):
        os.makedirs('docs')
        
    with open(output_path, 'w') as f:
        f.write(content)
    
    print("✅ Success! Single-file documentation generated in /docs/index.html")

if __name__ == "__main__":
    generate_static_docs()