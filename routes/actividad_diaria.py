from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db
from .mascota import Mascota  # si Mascota está en mascota.py dentro del mismo paquete


actividad_bp = Blueprint('actividad_diaria', __name__)

class ActividadDiaria(db.Model):
    __tablename__ = 'actividad_diaria'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    comidas_programadas = db.Column(db.Integer)
    comidas_cumplidas = db.Column(db.Integer)
    actividad_realizada = db.Column(db.Boolean)
    tiempo_actividad = db.Column(db.Integer)  # en minutos
    observaciones = db.Column(db.Text)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Crear actividad diaria
@actividad_bp.route('/actividades', methods=['POST'])
def crear_actividad():
    data = request.json
    if 'fecha' in data:
        # Opción 1: parsear fecha y hora completa, luego extraer solo la fecha
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%dT%H:%M:%S').date()
        
        # Alternativamente, opción 2:
        # fecha_str = data['fecha'].split('T')[0]
        # data['fecha'] = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
    nueva = ActividadDiaria(**data)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Actividad creada', 'id': nueva.id}), 201

# Obtener actividad diaria por ID
@actividad_bp.route('/actividades/<int:id>', methods=['GET'])
def obtener_actividad(id):
    actividad = ActividadDiaria.query.get_or_404(id)
    return jsonify({
        'id': actividad.id,
        'fecha': actividad.fecha.isoformat(),
        'comidas_programadas': actividad.comidas_programadas,
        'comidas_cumplidas': actividad.comidas_cumplidas,
        'actividad_realizada': actividad.actividad_realizada,
        'tiempo_actividad': actividad.tiempo_actividad,
        'observaciones': actividad.observaciones,
        'mascota_id': actividad.mascota_id
    })

# Actualizar actividad diaria
@actividad_bp.route('/actividades/<int:id>', methods=['PUT'])
def actualizar_actividad(id):
    actividad = ActividadDiaria.query.get_or_404(id)
    data = request.json
    if 'fecha' in data:
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    for campo, valor in data.items():
        setattr(actividad, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Actividad actualizada'})

# Eliminar actividad diaria
@actividad_bp.route('/actividades/<int:id>', methods=['DELETE'])
def eliminar_actividad(id):
    actividad = ActividadDiaria.query.get_or_404(id)
    db.session.delete(actividad)
    db.session.commit()
    return jsonify({'mensaje': 'Actividad eliminada'})


@actividad_bp.route('/actividades/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_actividades_por_cuidador(cuidador_id):
    actividades = (
        db.session.query(ActividadDiaria)
        .join(Mascota)
        .filter(Mascota.cuidador_id == cuidador_id)
        .all()
    )
    resultado = []
    for a in actividades:
        resultado.append({
            'id': a.id,
            'fecha': a.fecha.isoformat() if a.fecha else None,
            'comidas_programadas': a.comidas_programadas,
            'comidas_cumplidas': a.comidas_cumplidas,
            'actividad_realizada': a.actividad_realizada,
            'tiempo_actividad': a.tiempo_actividad,
            'observaciones': a.observaciones,
            'mascota_id': a.mascota_id
        })
    return jsonify(resultado)
