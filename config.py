import os

# URL completa de conexión a la base de datos PostgreSQL
DB_USER = os.getenv('DB_USER', 'mascotas')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mascotas123')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'app_mascotas')
DB_SCHEMA = os.getenv('DB_SCHEMA', 'app_mascotas')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?options=-csearch_path%3D{DB_SCHEMA}"

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Clave secreta para Flask (sessions, seguridad, etc.)
SECRET_KEY = os.getenv('SECRET_KEY', 'una_clave_secreta_para_tu_app')
