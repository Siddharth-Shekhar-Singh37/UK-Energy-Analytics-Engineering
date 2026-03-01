import os
import glob
import logging
import pandas as pd
import kagglehub
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# 1. Professional Logging Setup
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()

def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv('SNOW_USER'),
        password=os.getenv('SNOW_PASS'),
        account=os.getenv('SNOW_ACCOUNT'),
        warehouse=os.getenv('SNOW_WAREHOUSE'),
        database=os.getenv('SNOW_DATABASE'),
        schema=os.getenv('SNOW_SCHEMA')
    )

def load_partitioned_data():
    """Locates the partitioned block files and loads them into Snowflake."""
    
    try:
        logging.info("🔍 Requesting dataset location from Kaggle...")
        data_path = kagglehub.dataset_download("jeanmidev/smart-meters-in-london")
        
        # Path to the daily blocks based on your ls -R output
        blocks_dir = os.path.join(data_path, "daily_dataset", "daily_dataset")
        
        # Get all block files (block_0.csv, block_1.csv, etc.)
        block_files = glob.glob(os.path.join(blocks_dir, "block_*.csv"))
        block_files.sort() # Ensure we load them in order
        
        if not block_files:
            logging.error(f"❌ No block files found in {blocks_dir}")
            return
        
        logging.info(f"✅ Found {len(block_files)} data partitions (blocks) to load.")

        conn = get_snowflake_conn()
        logging.info("🚀 Snowflake connection established.")

        for i, file_path in enumerate(block_files):
            file_name = os.path.basename(file_path)
            logging.info(f"📦 Loading {file_name} ({i+1}/{len(block_files)})...")
            
            # Read the individual block
            df = pd.read_csv(file_path)
            
            # Standardize column names (Snowflake prefers uppercase)
            df.columns = [col.upper() for col in df.columns]

            # Write to Snowflake
            # auto_create_table=True only on the very first file
            success, nchunks, nrows, _ = write_pandas(
                conn=conn,
                df=df,
                table_name='LONDON_ENERGY_RAW',
                auto_create_table=(i == 0),
                quote_identifiers=False
            )
            logging.info(f"✅ Successfully loaded {nrows} rows from {file_name}.")
            
    except Exception as e:
        logging.error(f"❌ Ingestion failed: {e}")
        
    finally:
        if 'conn' in locals():
            conn.close()
            logging.info("🔒 Snowflake connection closed.")

if __name__ == "__main__":
    load_partitioned_data()