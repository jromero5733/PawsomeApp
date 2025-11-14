from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from database import db
from .mascota import Mascota

desparasitacion_bp = Blueprint('desparasitacion', __name__)

class Desparasitacion(db.Model):
    __tablename__ = 'desparasitacion'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20))
    producto_utilizado = db.Column(db.String(100))
    fecha_aplicacion = db.Column(db.Date)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Crear desparasitacion
@desparasitacion_bp.route('/desparasitaciones', methods=['POST'])
def crear_desparasitacion():
    data = request.json
    if 'fecha' in data:
        # Opción 1: parsear fecha y hora completa, luego extraer solo la fecha
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%dT%H:%M:%S').date()
        
    nueva = Desparasitacion(**data)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Desparasitacion creada', 'id': nueva.id}), 201

# Obtener desparasitacion por ID
@desparasitacion_bp.route('/desparasitaciones/<int:id>', methods=['GET'])
def obtener_desparasitacion(id):
    desparasitacion = Desparasitacion.query.get_or_404(id)
    return jsonify({
        'id': desparasitacion.id,
        'tipo': desparasitacion.tipo,
        'producto_utilizado': desparasitacion.producto_utilizado,
        'fecha_aplicacion': desparasitacion.fecha_aplicacion.isoformat() if desparasitacion.fecha_aplicacion else None,
        'mascota_id': desparasitacion.mascota_id
    })

# Actualizar desparasitacion
@desparasitacion_bp.route('/desparasitaciones/<int:id>', methods=['PUT'])
def actualizar_desparasitacion(id):
    desparasitacion = Desparasitacion.query.get_or_404(id)
    data = request.json
    if 'fecha' in data:
        # Opción 1: parsear fecha y hora completa, luego extraer solo la fecha
        data['fecha'] = datetime.strptime(data['fecha'], '%Y-%m-%dT%H:%M:%S').date()
    for campo, valor in data.items():
        setattr(desparasitacion, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Desparasitacion actualizada'})

# Eliminar desparasitacion
@desparasitacion_bp.route('/desparasitaciones/<int:id>', methods=['DELETE'])
def eliminar_desparasitacion(id):
    desparasitacion = Desparasitacion.query.get_or_404(id)
    db.session.delete(desparasitacion)
    db.session.commit()
    return jsonify({'mensaje': 'Desparasitacion eliminada'})

@desparasitacion_bp.route('/desparasitaciones/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_desparasitaciones_por_cuidador(cuidador_id):
    desparasitaciones = (
        db.session.query(Desparasitacion)
        .join(Mascota)
        .filter(Mascota.cuidador_id == cuidador_id)
        .all()
    )
    resultado = []
    for d in desparasitaciones:
        resultado.append({
            'id': d.id,
            'tipo': d.tipo,
            'producto_utilizado': d.producto_utilizado,
            'fecha_aplicacion': d.fecha_aplicacion.isoformat() if d.fecha_aplicacion else None,
            'mascota_id': d.mascota_id
        })
    return jsonify(resultado)
