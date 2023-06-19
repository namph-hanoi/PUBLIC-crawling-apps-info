import os
import sys
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = str(Path(Path(__file__).parent.name + '/../.env').resolve())
load_dotenv(dotenv_path)


class Config:
    NAME = os.getenv('APP_NAME', 'CRAWLING')
    DEBUG = bool(os.getenv('FLASK_DEBUG', False))
    APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
    APP_PORT = os.getenv('APP_PORT', '5002')