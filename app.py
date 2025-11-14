from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from database import db
import config
from flask_cors import CORS

app = Flask(__name__) # Initialize Flask app once
app.config.from_object(config) # Load configuration
db.init_app(app) # Initialize SQLAlchemy with the app
CORS(app) # Enable CORS for your app

with app.app_context():
    db.create_all() # Create database tables if they don't exist

# Import blueprints from the routes folder
from routes.cuidador import cuidador_bp
from routes.mascota import mascota_bp
from routes.vacuna import vacuna_bp
from routes.visita_veterinaria import visita_bp
from routes.desparasitacion import desparasitacion_bp
from routes.recordatorio import recordatorio_bp
from routes.actividad_diaria import actividad_bp
from routes.recomendacion import recomendacion_bp

# Register the blueprints
app.register_blueprint(cuidador_bp, url_prefix='/api')
app.register_blueprint(mascota_bp, url_prefix='/api')
app.register_blueprint(vacuna_bp, url_prefix='/api')
app.register_blueprint(visita_bp, url_prefix='/api')
app.register_blueprint(desparasitacion_bp, url_prefix='/api')
app.register_blueprint(recordatorio_bp, url_prefix='/api')
app.register_blueprint(actividad_bp, url_prefix='/api')
app.register_blueprint(recomendacion_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)