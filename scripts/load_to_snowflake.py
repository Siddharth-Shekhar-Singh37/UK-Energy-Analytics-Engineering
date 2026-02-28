import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import logging

# 1. Professional Logging Setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# 2. Load Environment Variables
load_dotenv()

def get_snowflake_conn():
    """Establishing a secure connection to Snowflake."""
    return snowflake.connector.connect(
        user=os.getenv('SNOW_USER'),
        password=os.getenv('SNOW_PASS'),
        account=os.getenv('SNOW_ACCOUNT'),
        warehouse=os.getenv('SNOW_WAREHOUSE'),
        database=os.getenv('SNOW_DATABASE'),
        schema=os.getenv('SNOW_SCHEMA')
    )

def load_large_csv_to_snowflake():
    """Loading CSV in chunks to prevent memory overflow."""
    
    data_path = '/home/codespace/.cache/kagglehub/datasets/jeanmidev/smart-meters-in-london/versions/3'
    file_path = f"{data_path}/LCL-FullReader.csv"
    
    conn = get_snowflake_conn()
    
    try:
        logging.info("🚀 Starting high-volume ingestion in chunks...")
        
        # We read in chunks of 100,000 rows
        chunk_size = 100000
        reader = pd.read_csv(file_path, chunksize=chunk_size)
        
        for i, chunk in enumerate(reader):
            logging.info(f"📦 Processing chunk {i+1}...")
            
            # Write each chunk to Snowflake
            success, nchunks, nrows, _ = write_pandas(
                conn=conn,
                df=chunk,
                table_name='LONDON_ENERGY_RAW',
                auto_create_table=(i == 0), # Only create table on the first chunk
                quote_identifiers=False
            )
            logging.info(f"✅ Successfully loaded {nrows} rows.")
            
    except Exception as e:
        logging.error(f"❌ Ingestion failed: {e}")
    finally:
        conn.close()
        logging.info("🔒 Snowflake connection closed.")

if __name__ == "__main__":
    load_large_csv_to_snowflake()