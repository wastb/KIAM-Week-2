import os
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load the database properties
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def load_data_from_postgres(query):

    # Load data from a postgres database
    try:
        #Establish connection to the database
        import pg8000

        conn = pg8000.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )

    
        df = pd.read_sql_query(query, conn)

        print("Data successfully imported from postgres")
        
        # Close the connection
        conn.close()
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
                
