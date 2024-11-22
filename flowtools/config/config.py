import os

# Rutas principales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(BASE_DIR, "../tmp")
CLOUD_DIR = os.path.join(BASE_DIR, "../screenshots")
LOG_DIR = os.path.join(BASE_DIR, "../logs")

# Base de datos
MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/tapestryflow?retryWrites=true&w=majority"

# Configuración del logger
LOG_FILE = os.path.join(LOG_DIR, "app.log")
