import os
import shutil
from PIL import ImageGrab
from datetime import datetime
from gridfs import GridFS
import ttkbootstrap as ttk
from tkinter import BOTH, Toplevel, Canvas
from snaplog.config.config import TMP_DIR, CLOUD_DIR
from snaplog.app.database import db  # Importar db
from snaplog.config.logger_config import setup_logger  # Importar la configuración del logger

# Inicializar el logger
logger = setup_logger()

# Inicializar GridFS
fs = GridFS(db)

class SnippingTool:
    def __init__(self, parent):
        self.parent = parent
        self.start_x = None
        self.start_y = None
        self.rect_id = None

    def clean_tmp_dir(self):
        """Elimina todos los archivos temporales en el directorio tmp."""
        if not os.path.exists(TMP_DIR):
            os.makedirs(TMP_DIR)
            logger.info(f"Directorio temporal creado en {TMP_DIR}")
        
        # Eliminar los archivos en TMP_DIR
        for filename in os.listdir(TMP_DIR):
            file_path = os.path.join(TMP_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                logger.info(f"Archivo temporal eliminado: {file_path}")
            else:
                logger.warning(f"Se omitió el archivo, no es un archivo regular: {file_path}")

    def start_snipping(self):
        """Inicia la herramienta de captura de pantalla."""
        self.clean_tmp_dir()  # Limpia el directorio tmp antes de tomar una nueva captura
        logger.info("Iniciando captura de pantalla...")

        # Crea una ventana a pantalla completa para la captura
        self.root = Toplevel()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)  # Fondo más oscuro
        self.root.config(bg="black")

        # Crea un lienzo para la selección
        canvas = Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        canvas.pack(fill=BOTH, expand=True)

        # Definir los eventos del mouse
        def on_button_press(event):
            """Inicia la selección de área al presionar el botón izquierdo del mouse."""
            self.start_x = event.x
            self.start_y = event.y
            logger.info(f"Inicio de selección en: ({self.start_x}, {self.start_y})")
            # Crear un rectángulo para el área de selección
            self.rect_id = canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

        def on_mouse_drag(event):
            """Actualiza las coordenadas del rectángulo mientras se arrastra el mouse."""
            canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

        def on_button_release(event):
            """Finaliza la selección del área y guarda la captura."""
            x1 = min(self.start_x, event.x)
            y1 = min(self.start_y, event.y)
            x2 = max(self.start_x, event.x)
            y2 = max(self.start_y, event.y)

            # Captura el área seleccionada
            capture_area = (x1, y1, x2, y2)
            tmp_file_path = os.path.join(TMP_DIR, f"capture_tmp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            try:
                ImageGrab.grab(bbox=capture_area).save(tmp_file_path)
                logger.info(f"Captura guardada temporalmente en: {tmp_file_path}")
            except Exception as e:
                logger.error(f"Error al guardar la captura: {e}")
                return

            # Mover al directorio de la nube y guardar en GridFS
            cloud_file_path = self.move_to_screenshots(tmp_file_path)
            gridfs_id = self.save_to_gridfs(cloud_file_path)

            # Notificar al padre y restaurar la ventana principal
            self.parent.update_capture_path(tmp_file_path, cloud_file_path, gridfs_id)
            logger.info(f"Captura guardada en GridFS con ID: {gridfs_id}")
            self.root.destroy()
            self.parent.root.deiconify()

        # Vincular los eventos del mouse
        canvas.bind("<ButtonPress-1>", on_button_press)
        canvas.bind("<B1-Motion>", on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", on_button_release)

        # Ocultar la ventana principal y mostrar la herramienta de captura
        self.parent.root.withdraw()
        self.root.mainloop()

    def move_to_screenshots(self, file_path):
        """Mueve la captura al directorio local permanente."""
        if not os.path.exists(CLOUD_DIR):
            os.makedirs(CLOUD_DIR)  # Crea el directorio si no existe
            logger.info(f"Directorio de capturas creado en: {CLOUD_DIR}")
        
        final_path = os.path.join(CLOUD_DIR, os.path.basename(file_path))
        shutil.move(file_path, final_path)
        logger.info(f"Captura movida a: {final_path}")
        return final_path

    def save_to_gridfs(self, file_path):
        """Guarda la captura en GridFS y devuelve el ID."""
        try:
            with open(file_path, "rb") as file:
                gridfs_id = fs.put(file, filename=os.path.basename(file_path), uploadDate=datetime.now())
            logger.info(f"Captura guardada en GridFS con ID: {gridfs_id}")
            return gridfs_id
        except Exception as e:
            logger.error(f"Error al guardar la captura en GridFS: {e}")
            raise e  # Vuelve a lanzar la excepción para que se pueda manejar fuera de la clase

