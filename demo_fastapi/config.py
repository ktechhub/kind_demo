import os
from pathlib import Path
from dotenv import load_dotenv

# BASE DIRECTORY PATH
BASE_DIR = Path(__file__).resolve().parent.parent

## Load env
load_dotenv()

## get variables
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

api_version = os.getenv("API_VERSION", "1.0.0")
contact = {
    "name": "DemoFastapi",
    "url": "http://demofastapi.com/contact/",
    "email": "info@demofastapi.com",
}


ENV = os.getenv("ENV", "dev").replace(" ", "")

if ENV == "dev":
    RELOAD = True
    LOG_LEVEL = "debug"
    ALLOWED_HOSTS = ["*"]  # Get the allowed hosts
else:
    RELOAD = False
    LOG_LEVEL = "info"
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
