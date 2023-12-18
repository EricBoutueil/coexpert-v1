import os
from os import path

TARGET = "cloud"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

PDF_NBER = 11
PDF_PATH = path.join(os.path.dirname(__file__), 'raw_data', f'{PDF_NBER}_pdf')
