import logging
from ttkbootstrap import Window
from snaplog.app.ui import BugReportWindow
from snaplog.app.database import initialize_database
from snaplog.config.logger_config import setup_logger

# Configurar el logger
logger = setup_logger()

def main():
    try:
        # Inicializar la base de datos
        initialize_database()
        logger.info("Base de datos inicializada correctamente.")
        
        # Crear la ventana principal
        root = Window(themename="darkly")
        BugReportWindow(root)
        logger.info("Ventana de la aplicación iniciada correctamente.")
        
        # Iniciar la interfaz gráfica
        root.mainloop()
        logger.info("Interfaz gráfica en ejecución.")
    
    except Exception as e:
        logger.error(f"Error durante la ejecución de la aplicación: {e}")

if __name__ == "__main__":
    main()
