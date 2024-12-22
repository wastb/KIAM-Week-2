import os
import pandas as pd
import pg8000

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Load the database properties
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def to_postgre(df, table_name):
    # Export the data postgres database
    try:
        #Establish connection to the database
        
        engine = create_engine(f"postgresql+pg8000://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

        print("DataFrame exported successfully!")
       
    except Exception as e:
        print(f"An error occurred: {e}")