import kagglehub
import os

# 1. This automatically looks for the KAGGLE_API_TOKEN you just exported
print("🚀 Starting download from Kaggle...")
path = kagglehub.dataset_download("jeanmidev/smart-meters-in-london")

print(f"\n✅ SUCCESS! Data is now in your Cloud Bridge: {path}")

# 2. Let's see exactly what files we have to work with
files = os.listdir(path)
print("\nFiles ready for Snowflake:")
for f in files:
    print(f"- {f}")
    