from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db
from .mascota import Mascota

visita_bp = Blueprint('visita_veterinaria', __name__)

class VisitaVeterinaria(db.Model):
    __tablename__ = 'visita_veterinaria'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.Text, nullable=False)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Crear visita veterinaria
@visita_bp.route('/visitas', methods=['POST'])
def crear_visita():
    data = request.json
    if 'fecha' in data:
        # Opción 1: parsear fecha y hora completa, luego extraer solo la fecha
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%dT%H:%M:%S').date()
    nueva = VisitaVeterinaria(**data)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Visita creada', 'id': nueva.id}), 201

# Obtener visita veterinaria por ID
@visita_bp.route('/visitas/<int:id>', methods=['GET'])
def obtener_visita(id):
    visita = VisitaVeterinaria.query.get_or_404(id)
    return jsonify({
        'id': visita.id,
        'fecha': visita.fecha.isoformat(),
        'motivo': visita.motivo,
        'mascota_id': visita.mascota_id
    })

# Actualizar visita veterinaria
@visita_bp.route('/visitas/<int:id>', methods=['PUT'])
def actualizar_visita(id):
    visita = VisitaVeterinaria.query.get_or_404(id)
    data = request.json
    if 'fecha' in data:
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
    for campo, valor in data.items():
        setattr(visita, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Visita actualizada'})

# Eliminar visita veterinaria
@visita_bp.route('/visitas/<int:id>', methods=['DELETE'])
def eliminar_visita(id):
    visita = VisitaVeterinaria.query.get_or_404(id)
    db.session.delete(visita)
    db.session.commit()
    return jsonify({'mensaje': 'Visita eliminada'})


@visita_bp.route('/visitas/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_visitas_por_cuidador(cuidador_id):
    visitas = (
        db.session.query(VisitaVeterinaria)
        .join(Mascota)
        .filter(Mascota.cuidador_id == cuidador_id)
        .all()
    )
    resultado = []
    for v in visitas:
        resultado.append({
            'id': v.id,
            'fecha': v.fecha.isoformat() if v.fecha else None,
            'motivo': v.motivo,
            'mascota_id': v.mascota_id
        })
    return jsonify(resultado)
