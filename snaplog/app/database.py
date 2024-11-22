from pymongo import MongoClient
from snaplog.config.config import MONGO_URI
from snaplog.config.logger_config import setup_logger

# Configurar el logger
logger = setup_logger()

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client["tapestryflow"]  # Nombre de la base de datos

# Colecciones
projects_collection = db.projects
stories_collection = db.stories
tasks_collection = db.tasks
reports_collection = db.reports

def initialize_database():
    """Inicializa la base de datos con datos de ejemplo si está vacía."""
    try:
        if projects_collection.count_documents({}) == 0:
            projects = [
                {"name": "Proyecto A"},
                {"name": "Proyecto B"},
            ]
            projects_collection.insert_many(projects)
            logger.info("Proyectos iniciales insertados en la base de datos.")

        if stories_collection.count_documents({}) == 0:
            stories = [
                {"title": "Historia 1", "project": "Proyecto A"},
                {"title": "Historia 2", "project": "Proyecto B"},
            ]
            stories_collection.insert_many(stories)
            logger.info("Historias iniciales insertadas en la base de datos.")

        if tasks_collection.count_documents({}) == 0:
            tasks = [
                {"name": "Tarea 1.1", "story": "Historia 1"},
                {"name": "Tarea 1.2", "story": "Historia 1"},
                {"name": "Tarea 2.1", "story": "Historia 2"},
                {"name": "Tarea 2.2", "story": "Historia 2"},
            ]
            tasks_collection.insert_many(tasks)
            logger.info("Tareas iniciales insertadas en la base de datos.")

    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {e}")

def get_projects():
    """Obtiene todos los proyectos disponibles."""
    try:
        projects = [project["name"] for project in projects_collection.find()]
        logger.info(f"Proyectos obtenidos: {projects}")
        return projects
    except Exception as e:
        logger.error(f"Error al obtener proyectos: {e}")
        return []

def get_stories(project_name):
    """Obtiene todas las historias relacionadas con un proyecto."""
    try:
        stories = list(stories_collection.find({"project": project_name}, {"_id": 0, "title": 1}))
        logger.info(f"Historias obtenidas para el proyecto {project_name}: {stories}")
        return stories
    except Exception as e:
        logger.error(f"Error al obtener historias para el proyecto {project_name}: {e}")
        return []

def get_tasks_by_story(story_title):
    """Obtiene todas las tareas relacionadas con una historia."""
    try:
        tasks = list(tasks_collection.find({"story": story_title}, {"_id": 0, "name": 1}))
        logger.info(f"Tareas obtenidas para la historia {story_title}: {tasks}")
        return tasks
    except Exception as e:
        logger.error(f"Error al obtener tareas para la historia {story_title}: {e}")
        return []

def save_bug_report(report_data):
    """Guarda un reporte de bug en la base de datos."""
    try:
        reports_collection.insert_one(report_data)
        logger.info(f"Reporte de bug guardado: {report_data}")
    except Exception as e:
        logger.error(f"Error al guardar el reporte de bug: {e}")
