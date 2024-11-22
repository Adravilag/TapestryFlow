from pymongo import MongoClient
from config.config import MONGO_URI

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client["tapestryflow"]

# Definir colecciones
projects_collection = db.projects
users_collection = db.users
tasks_collection = db.tasks
reports_collection = db.reports
