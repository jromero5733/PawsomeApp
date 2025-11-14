from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db
from .mascota import Mascota

recordatorio_bp = Blueprint('recordatorio', __name__)

class Recordatorio(db.Model):
    __tablename__ = 'recordatorio'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    fecha_hora = db.Column(db.DateTime)
    estado = db.Column(db.String(20))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Crear recordatorio
@recordatorio_bp.route('/recordatorios', methods=['POST'])
def crear_recordatorio():
    data = request.json
    if 'fecha_hora' in data and data['fecha_hora']:
        data['fecha_hora'] = datetime.strptime(data['fecha_hora'], '%Y-%m-%dT%H:%M:%S')
    nuevo = Recordatorio(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Recordatorio creado', 'id': nuevo.id}), 201

# Obtener recordatorio por ID
@recordatorio_bp.route('/recordatorios/<int:id>', methods=['GET'])
def obtener_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    return jsonify({
        'id': recordatorio.id,
        'titulo': recordatorio.titulo,
        'tipo': recordatorio.tipo,
        'fecha_hora': recordatorio.fecha_hora.isoformat() if recordatorio.fecha_hora else None,
        'estado': recordatorio.estado,
        'mascota_id': recordatorio.mascota_id
    })

# Actualizar recordatorio
@recordatorio_bp.route('/recordatorios/<int:id>', methods=['PUT'])
def actualizar_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    data = request.json
    if 'fecha_hora' in data and data['fecha_hora']:
        data['fecha_hora'] = datetime.strptime(data['fecha_hora'], '%Y-%m-%dT%H:%M:%S')
    for campo, valor in data.items():
        setattr(recordatorio, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Recordatorio actualizado'})

# Eliminar recordatorio
@recordatorio_bp.route('/recordatorios/<int:id>', methods=['DELETE'])
def eliminar_recordatorio(id):
    recordatorio = Recordatorio.query.get_or_404(id)
    db.session.delete(recordatorio)
    db.session.commit()
    return jsonify({'mensaje': 'Recordatorio eliminado'})


@recordatorio_bp.route('/recordatorios/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_recordatorios_por_cuidador(cuidador_id):
    recordatorios = (
        db.session.query(Recordatorio)
        .join(Mascota)
        .filter(Mascota.cuidador_id == cuidador_id)
        .all()
    )
    resultado = []
    for r in recordatorios:
        resultado.append({
            'id': r.id,
            'titulo': r.titulo,
            'tipo': r.tipo,
            'fecha_hora': r.fecha_hora.isoformat() if r.fecha_hora else None,
            'estado': r.estado,
            'mascota_id': r.mascota_id
        })
    return jsonify(resultado)
