import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Configuración
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
CLOUD_DIR = os.getenv("CLOUD_DIR", "./screenshots")
TMP_DIR = os.getenv("TMP_DIR", "./tmp")