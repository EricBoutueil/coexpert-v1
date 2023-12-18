import os
from os import path

TARGET = "local"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PDF_NBER = 2
PDF_PATH = path.join(os.path.dirname(__file__), 'raw_data', f'{PDF_NBER}_pdf')
