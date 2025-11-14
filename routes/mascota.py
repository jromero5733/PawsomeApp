
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db


mascota_bp = Blueprint('mascota', __name__)

class Mascota(db.Model):
    __tablename__ = 'mascota'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(20))
    raza = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    sexo = db.Column(db.String(10))
    peso = db.Column(db.Numeric(5,2))
    cuidador_id = db.Column(db.Integer, db.ForeignKey('cuidador.id'), nullable=False)

# Crear mascota
@mascota_bp.route('/mascotas', methods=['POST'])
def crear_mascota():
    data = request.json
    nueva = Mascota(**data)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Mascota creada', 'id': nueva.id}), 201

# Obtener mascota por ID
@mascota_bp.route('/mascotas/<int:id>', methods=['GET'])
def obtener_mascota(id):
    mascota = Mascota.query.get_or_404(id)
    return jsonify({
        'id': mascota.id,
        'nombre': mascota.nombre,
        'especie': mascota.especie,
        'raza': mascota.raza,
        'fecha_nacimiento': mascota.fecha_nacimiento.isoformat() if mascota.fecha_nacimiento else None,
        'sexo': mascota.sexo,
        'peso': float(mascota.peso) if mascota.peso else None,
        'cuidador_id': mascota.cuidador_id
    })

# Actualizar mascota
@mascota_bp.route('/mascotas/<int:id>', methods=['PUT'])
def actualizar_mascota(id):
    mascota = Mascota.query.get_or_404(id)
    data = request.json
    for campo, valor in data.items():
        setattr(mascota, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Mascota actualizada'})

# Eliminar mascota
@mascota_bp.route('/mascotas/<int:id>', methods=['DELETE'])
def eliminar_mascota(id):
    mascota = Mascota.query.get_or_404(id)
    db.session.delete(mascota)
    db.session.commit()
    return jsonify({'mensaje': 'Mascota eliminada'})


@mascota_bp.route('/mascotas/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_mascotas_por_cuidador(cuidador_id):
    mascotas = Mascota.query.filter_by(cuidador_id=cuidador_id).all()
    resultado = []
    for m in mascotas:
        resultado.append({
            'id': m.id,
            'nombre': m.nombre,
            'especie': m.especie,
            'raza': m.raza,
            'fecha_nacimiento': m.fecha_nacimiento.isoformat() if m.fecha_nacimiento else None,
            'sexo': m.sexo,
            'peso': m.peso,
            'cuidador_id': m.cuidador_id
        })
    return jsonify(resultado)
