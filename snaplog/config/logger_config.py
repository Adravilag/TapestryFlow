# config/logger_config.py
import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Configuración de tamaño máximo de archivo de log
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB (ajustable)
LOG_BACKUP_COUNT = 5  # Número de archivos de log a mantener (ajustable)

# Obtener la ruta absoluta del directorio de logs
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)  # Crear el directorio si no existe

# Nombre del archivo de log con la fecha actual
log_filename = datetime.now().strftime("SnapLog_%Y%m%d_%H%M%S.log")
LOG_FILE = os.path.join(LOG_DIR, log_filename)

def setup_logger():
    """Configura y devuelve un logger con salida en consola y rotación de logs."""
    logger = logging.getLogger('SnapLog')

    # Verificar si el logger ya tiene handlers configurados
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)  # Nivel de log global (puedes cambiar a INFO, ERROR, etc.)
        
        # Crear un manejador de archivo con rotación
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=LOG_BACKUP_COUNT)
        file_handler.setLevel(logging.DEBUG)  # Nivel de log para el archivo de log
        
        # Crear un manejador de consola para ver los logs en la terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Nivel de log para la consola

        # Crear un formato para los logs que incluye el archivo, línea y la función
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(filename)s - Line: %(lineno)d - Function: %(funcName)s')
        
        # Asignar el formato a ambos manejadores
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Añadir los manejadores al logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger
