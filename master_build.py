import os
import subprocess
import json
from dotenv import load_dotenv

def run_command(cmd):
    """Utility to run terminal commands and show output."""
    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ ERROR: {result.stderr}")
        return False
    print(result.stdout)
    return True

def build():
    # 1. Load the secrets correctly from .env
    load_dotenv()
    
    # 2. Re-create the folder structure
    if not os.path.exists('docs'):
        os.makedirs('docs')
        print("Created docs folder.")

    # 3. Run dbt Docs Generate
    print("🚀 Generating dbt artifacts...")
    dbt_cmd = ["dbt", "docs", "generate", "--profiles-dir", "."]
    if not run_command(dbt_cmd):
        return

    # 4. Stitch the files (The "Senior" trick)
    print("🪄 Stitching artifacts into single-file index.html...")
    try:
        with open('target/index.html', 'r') as f:
            content = f.read()
        with open('target/manifest.json', 'r') as f:
            manifest = json.load(f)
        with open('target/catalog.json', 'r') as f:
            catalog = json.load(f)

        content = content.replace('report_type: "regular"', 'report_type: "static"')
        manifest_string = json.dumps(manifest).replace('"', '\\"')
        content = content.replace('var o = {manifest: "REPLACE_ME_MANIFEST", catalog: "REPLACE_ME_CATALOG"};', 
                                  f'var o = {{manifest: "{manifest_string}", catalog: "REPLACE_ME_CATALOG"}};')
        catalog_string = json.dumps(catalog).replace('"', '\\"')
        content = content.replace('catalog: "REPLACE_ME_CATALOG"', f'catalog: "{catalog_string}"')

        with open('docs/index.html', 'w') as f:
            f.write(content)
        print("✅ Stitching successful!")
    except Exception as e:
        print(f"❌ Stitching failed: {e}")
        return

    # 5. Push to GitHub
    print("📤 Pushing to GitHub...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "DOCS: final end-to-end documentation build via master script"])
    subprocess.run(["git", "push", "origin", "main"])
    print("\n🏁 MISSION COMPLETE. Wait 60 seconds, then Hard-Refresh your website (Ctrl+F5).")

if __name__ == "__main__":
    build()