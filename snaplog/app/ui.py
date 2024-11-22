import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from tkinter import filedialog, messagebox
import os
from datetime import datetime
from snaplog.app.capture import SnippingTool
from snaplog.app.database import get_stories, get_tasks_by_story, save_bug_report, get_projects
from snaplog.config.logger_config import setup_logger

# Configurar logger
logger = setup_logger()

class BugReportWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reporte de Bug - Dashboard")

        # Dimensiones de la ventana
        window_width = 800
        window_height = 600

        # Centrar la ventana en la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.root.resizable(False, False)

        self.capture_path = None
        self.attachment_path = None

        # Diseño Moderno - Tema Oscuro
        self.style = ttk.Style(theme="darkly")

        # Scrollable Frame
        self.scrollable_frame = ScrolledFrame(self.root, autohide=True, padding=10)
        self.scrollable_frame.pack(fill=BOTH, expand=True)

        # Crear el formulario
        self.create_form(self.scrollable_frame)

        self.cloud_capture_id = None  # Inicializar el atributo

    def create_form(self, scrolled_frame):
        """Crea el formulario con los elementos de entrada."""
        # Reducir márgenes laterales con padding
        content_frame = ttk.Frame(scrolled_frame, padding=(10, 10))  # Reducir márgenes generales
        content_frame.pack(fill=BOTH, expand=True)

        # Título del problema
        ttk.Label(content_frame, text="Título del problema", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        self.title_entry = ttk.Entry(content_frame, width=80, bootstyle=INFO)
        self.title_entry.pack(pady=5, padx=5, fill=X)  # Añadir margen horizontal al Entry

        # Descripción del problema
        ttk.Label(content_frame, text="Descripción del problema", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        self.description_text = ttk.Text(content_frame, width=80, height=10, wrap="word")
        self.description_text.pack(pady=5, padx=5, fill=X)  # Añadir margen horizontal al Text

        # Opciones de prioridad
        ttk.Label(content_frame, text="Prioridad", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        self.priority_combobox = ttk.Combobox(content_frame, values=["Baja", "Media", "Alta"], state="readonly")
        self.priority_combobox.set("Media")
        self.priority_combobox.pack(pady=5, padx=5, fill=X)  # Margen horizontal

        # Selección de Proyecto
        ttk.Label(content_frame, text="Proyecto", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        self.project_combobox = ttk.Combobox(content_frame, state="readonly")
        self.project_combobox.pack(pady=5, padx=5, fill=X)  # Margen horizontal
        self.project_combobox.bind("<<ComboboxSelected>>", self.load_stories)

        # Selección de Historia
        ttk.Label(content_frame, text="Historia", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        self.story_combobox = ttk.Combobox(content_frame, state="readonly")
        self.story_combobox.pack(pady=5, padx=5, fill=X)  # Margen horizontal
        self.story_combobox.bind("<<ComboboxSelected>>", self.load_tasks)

        # Selección de Tarea
        ttk.Label(content_frame, text="Tarea", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        self.task_combobox = ttk.Combobox(content_frame, state="readonly")
        self.task_combobox.pack(pady=5, padx=5, fill=X)  # Margen horizontal

        # Captura de pantalla
        ttk.Label(content_frame, text="Captura de pantalla", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        capture_frame = ttk.Frame(content_frame, padding=(5, 0))  # Margen reducido
        capture_frame.pack(fill=X, pady=5)
        ttk.Button(capture_frame, text="Hacer captura", command=self.capture_screen, bootstyle=SUCCESS).pack(side=LEFT, padx=5)
        self.capture_preview_label = ttk.Label(capture_frame, text="Sin captura seleccionada", font=("Segoe UI", 10), foreground="gray")
        self.capture_preview_label.pack(side=LEFT, padx=10)

        # Adjuntar archivo
        ttk.Label(content_frame, text="Adjunto (opcional)", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=5)
        attach_frame = ttk.Frame(content_frame, padding=(5, 0))  # Margen reducido
        attach_frame.pack(fill=X, pady=5)
        ttk.Button(attach_frame, text="Adjuntar archivo", command=self.attach_file, bootstyle=INFO).pack(side=LEFT, padx=5)
        self.attachment_label = ttk.Label(attach_frame, text="No se ha adjuntado ningún archivo", font=("Segoe UI", 10), foreground="gray")
        self.attachment_label.pack(side=LEFT, padx=10)

        # Botones de acción
        button_frame = ttk.Frame(content_frame, padding=(5, 0))  # Margen reducido
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Enviar", command=self.submit_report, bootstyle=SUCCESS, width=20).pack(side=LEFT, padx=10)
        ttk.Button(button_frame, text="Cancelar", command=self.root.destroy, bootstyle=DANGER, width=20).pack(side=LEFT, padx=10)

        # Cargar proyectos e historias
        self.load_projects()

    def load_projects(self):
        """Carga los proyectos desde la base de datos."""
        try:
            logger.info("Cargando proyectos desde la base de datos.")
            projects = get_projects()
            self.project_combobox["values"] = projects
            if projects:
                self.project_combobox.set(projects[0])
            self.load_stories()
            logger.info("Proyectos cargados correctamente.")
        except Exception as e:
            logger.error(f"Error al cargar proyectos: {e}")

    def load_stories(self, event=None):
        """Carga las historias según el proyecto seleccionado."""
        try:
            selected_project = self.project_combobox.get()
            stories = get_stories(selected_project)
            story_titles = [story["title"] for story in stories]
            self.story_combobox["values"] = story_titles
            self.story_combobox.set("")
            self.load_tasks()
            logger.info(f"Historias cargadas para el proyecto '{selected_project}'.")
        except Exception as e:
            logger.error(f"Error al cargar historias: {e}")

    def load_tasks(self, event=None):
        """Carga las tareas según la historia seleccionada."""
        try:
            selected_story = self.story_combobox.get()
            tasks = get_tasks_by_story(selected_story)
            task_names = [task["name"] for task in tasks]
            self.task_combobox["values"] = task_names
            self.task_combobox.set("")
            logger.info(f"Tareas cargadas para la historia '{selected_story}'.")
        except Exception as e:
            logger.error(f"Error al cargar tareas: {e}")

    def capture_screen(self):
        """Oculta la ventana principal y realiza la captura."""
        try:
            logger.info("Iniciando captura de pantalla...")
            self.root.withdraw()  # Ocultar la ventana principal
            snipping_tool = SnippingTool(self)  # Inicia la herramienta de captura

            def restore_window():
                self.root.deiconify()  # Volver a mostrar la ventana principal

            # Inicia la captura y asegura que la ventana se restaure
            snipping_tool.start_snipping()
            self.root.after(100, restore_window)
            logger.info("Captura de pantalla completada.")
        except Exception as e:
            logger.error(f"Error al iniciar captura de pantalla: {e}")

    def update_capture_path(self, local_file_path, cloud_file_path, cloud_capture_id):
        """Actualiza las rutas de las capturas de pantalla."""
        self.capture_path = local_file_path
        self.cloud_path = cloud_file_path
        self.cloud_capture_id = cloud_capture_id  # Asigna el ID de la nube
        self.capture_preview_label.config(
            text=f"Captura seleccionada: {os.path.basename(local_file_path)}", foreground="white"
        )
        logger.info(f"Captura seleccionada: {os.path.basename(local_file_path)}")

    def attach_file(self):
        try:
            file_path = filedialog.askopenfilename(title="Seleccionar archivo")
            if file_path:
                self.attachment_path = file_path
                self.attachment_label.config(text=f"Archivo: {os.path.basename(file_path)}", foreground="white")
                logger.info(f"Archivo adjunto: {os.path.basename(file_path)}")
        except Exception as e:
            logger.error(f"Error al adjuntar archivo: {e}")

    def submit_report(self):
        """Registra el reporte."""
        try:
            title = self.title_entry.get().strip()
            description = self.description_text.get("1.0", "end").strip()
            priority = self.priority_combobox.get()
            project = self.project_combobox.get()
            story = self.story_combobox.get()
            task = self.task_combobox.get()

            if not title or not description or not project:
                messagebox.showerror("Error", "Por favor, completa todos los campos obligatorios.")
                return

            report_data = {
                "title": title,
                "description": description,
                "priority": priority,
                "project": project,
                "story": story,
                "task": task,
                "cloud_capture_id": self.cloud_capture_id,  # ID en la nube
                "created_at": datetime.now(),
            }

            save_bug_report(report_data)
            messagebox.showinfo("Éxito", "Reporte registrado correctamente.")
            logger.info(f"Reporte registrado: {title} - {project}")
            self.root.destroy()
        except Exception as e:
            logger.error(f"Error al registrar el reporte: {e}")
            messagebox.showerror("Error", f"Error al registrar el reporte: {e}")
