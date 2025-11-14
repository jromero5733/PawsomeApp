from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db
from .mascota import Mascota

vacuna_bp = Blueprint('vacuna', __name__)

class Vacuna(db.Model):
    __tablename__ = 'vacuna'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    fecha_aplicacion = db.Column(db.Date, nullable=False)
    dosis = db.Column(db.String(50))
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Crear vacuna
@vacuna_bp.route('/vacunas', methods=['POST'])
def crear_vacuna():
    data = request.json
    if 'fecha' in data:
        # Opción 1: parsear fecha y hora completa, luego extraer solo la fecha
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%dT%H:%M:%S').date() 
    nueva = Vacuna(**data)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Vacuna creada', 'id': nueva.id}), 201

# Obtener vacuna por ID
@vacuna_bp.route('/vacunas/<int:id>', methods=['GET'])
def obtener_vacuna(id):
    vacuna = Vacuna.query.get_or_404(id)
    return jsonify({
        'id': vacuna.id,
        'tipo': vacuna.tipo,
        'fecha_aplicacion': vacuna.fecha_aplicacion.isoformat(),
        'dosis': vacuna.dosis,
        'mascota_id': vacuna.mascota_id
    })

# Actualizar vacuna
@vacuna_bp.route('/vacunas/<int:id>', methods=['PUT'])
def actualizar_vacuna(id):
    vacuna = Vacuna.query.get_or_404(id)
    data = request.json
    if 'fecha_aplicacion' in data:
        data['fecha_aplicacion'] = datetime.strptime(data['fecha_aplicacion'], '%Y-%m-%d').date()
    for campo, valor in data.items():
        setattr(vacuna, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Vacuna actualizada'})

# Eliminar vacuna
@vacuna_bp.route('/vacunas/<int:id>', methods=['DELETE'])
def eliminar_vacuna(id):
    vacuna = Vacuna.query.get_or_404(id)
    db.session.delete(vacuna)
    db.session.commit()
    return jsonify({'mensaje': 'Vacuna eliminada'})


@vacuna_bp.route('/vacunas/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_vacunas_por_cuidador(cuidador_id):
    vacunas = (
        db.session.query(Vacuna)
        .join(Mascota)
        .filter(Mascota.cuidador_id == cuidador_id)
        .all()
    )
    resultado = []
    for v in vacunas:
        resultado.append({
            'id': v.id,
            'tipo': v.tipo,
            'fecha_aplicacion': v.fecha_aplicacion.isoformat() if v.fecha_aplicacion else None,
            'dosis': v.dosis,
            'mascota_id': v.mascota_id
        })
    return jsonify(resultado)
