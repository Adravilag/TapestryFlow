import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from snaplog.config.logger_config import setup_logger  # Corregir la importación
from snaplog.app.ui import BugReportWindow

class DashboardView:
    def __init__(self, root):
        self.root = root
        self.root.title("TapestryFlow - Dashboard")
        self.root.geometry("1024x768")
        self.create_widgets()

    def create_widgets(self):
        # Título principal
        ttk.Label(self.root, text="Bienvenido a TapestryFlow", font=("Segoe UI", 16, "bold")).pack(pady=20)

        # Botones de acción
        ttk.Button(self.root, text="Gestión de Proyectos", command=self.open_project_manager).pack(pady=10)
        ttk.Button(self.root, text="Gestión de Usuarios", command=self.open_user_manager).pack(pady=10)

        # Botón para probar SnapLog (creará un log)
        ttk.Button(self.root, text="Probar SnapLog", command=self.test_snaplog).pack(pady=10)

    def open_project_manager(self):
        print("Abriendo gestor de proyectos...")

    def open_user_manager(self):
        print("Abriendo gestor de usuarios...")

    def test_snaplog(self):
        """Función para probar SnapLog al hacer un log de prueba y abrir su ventana."""
        logger = setup_logger()  # Configuramos el logger de SnapLog

        # Realizamos un log de prueba
        logger.info("Mensaje de prueba desde el Dashboard de TapestryFlow.")

        # Aquí abrimos la ventana de SnapLog (o lo que sea que SnapLog haga)
        snaplog_window = BugReportWindow(self.root)  # Suponiendo que BugReportWindow es la ventana principal de SnapLog
        snaplog_window.root.mainloop()  # Iniciar la ventana de SnapLog

        # Mensaje en la consola para confirmar la acción
        print("Prueba de SnapLog realizada exitosamente desde TapestryFlow.")
