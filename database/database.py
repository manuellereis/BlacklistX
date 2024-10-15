import os

from dotenv import load_dotenv

from sqlalchemy import create_engine

load_dotenv()

credentials = {
    "USERNAME": os.getenv("USERNAME"),
    "PASSWORD": os.getenv("PASSWORD"),
    "DNS": os.getenv("DNS"),
}

ENGINE = create_engine(f"mssql+pymssql://{credentials['USERNAME']}:{credentials['PASSWORD']}@{credentials['DNS']}/db_facialRecognition")