import os
import pandas as pd
import kagglehub
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv
import logging

# 1. Logging and Security Setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
load_dotenv()

def load_household_metadata():
    """Ingests the household metadata CSV into Snowflake."""
    
    # A. Locate the data dynamically
    logging.info("🔍 Locating metadata file...")
    data_path = kagglehub.dataset_download("jeanmidev/smart-meters-in-london")
    file_path = os.path.join(data_path, "informations_households.csv")
    
    if not os.path.exists(file_path):
        logging.error(f"❌ Could not find informations_households.csv at {file_path}")
        return

    # B. Read data into Pandas
    df = pd.read_csv(file_path)
    # Standardize column names to match our Snowflake table
    df.columns = ['LCLID', 'STDORTOU', 'ACORN', 'ACORN_GROUPED', 'FILE_NAME']

    # C. Establish Snowflake Connection
    conn = snowflake.connector.connect(
        user=os.getenv('SNOW_USER'),
        password=os.getenv('SNOW_PASS'),
        account=os.getenv('SNOW_ACCOUNT'),
        warehouse=os.getenv('SNOW_WAREHOUSE'),
        database=os.getenv('SNOW_DATABASE'),
        schema=os.getenv('SNOW_SCHEMA')
    )

    try:
        logging.info(f"🚀 Pushing {len(df)} household records to Snowflake...")
        
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name='LONDON_HOUSEHOLDS_RAW',
            auto_create_table=False, # We already created it via SQL
            quote_identifiers=False
        )
        
        logging.info(f"✅ Success! Loaded {nrows} rows into LONDON_HOUSEHOLDS_RAW.")

    except Exception as e:
        logging.error(f"❌ Ingestion failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    load_household_metadata()