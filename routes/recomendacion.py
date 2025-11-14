from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db
from .mascota import Mascota

recomendacion_bp = Blueprint('recomendacion', __name__)

class Recomendacion(db.Model):
    __tablename__ = 'recomendacion'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    texto = db.Column(db.Text)
    mascota_id = db.Column(db.Integer, db.ForeignKey('mascota.id'), nullable=False)

# Crear recomendacion
@recomendacion_bp.route('/recomendaciones', methods=['POST'])
def crear_recomendacion():
    data = request.json
    nueva = Recomendacion(**data)
    db.session.add(nueva)
    db.session.commit()
    return jsonify({'mensaje': 'Recomendación creada', 'id': nueva.id}), 201

# Obtener recomendacion por ID
@recomendacion_bp.route('/recomendaciones/<int:id>', methods=['GET'])
def obtener_recomendacion(id):
    recomendacion = Recomendacion.query.get_or_404(id)
    return jsonify({
        'id': recomendacion.id,
        'tipo': recomendacion.tipo,
        'texto': recomendacion.texto,
        'mascota_id': recomendacion.mascota_id
    })

# Actualizar recomendacion
@recomendacion_bp.route('/recomendaciones/<int:id>', methods=['PUT'])
def actualizar_recomendacion(id):
    recomendacion = Recomendacion.query.get_or_404(id)
    data = request.json
    for campo, valor in data.items():
        setattr(recomendacion, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Recomendación actualizada'})

# Eliminar recomendacion
@recomendacion_bp.route('/recomendaciones/<int:id>', methods=['DELETE'])
def eliminar_recomendacion(id):
    recomendacion = Recomendacion.query.get_or_404(id)
    db.session.delete(recomendacion)
    db.session.commit()
    return jsonify({'mensaje': 'Recomendación eliminada'})


@recomendacion_bp.route('/recomendaciones/cuidador/<int:cuidador_id>', methods=['GET'])
def obtener_recomendaciones_por_cuidador(cuidador_id):
    recomendaciones = (
        db.session.query(Recomendacion)
        .join(Mascota)
        .filter(Mascota.cuidador_id == cuidador_id)
        .all()
    )
    resultado = []
    for rec in recomendaciones:
        resultado.append({
            'id': rec.id,
            'tipo': rec.tipo,
            'texto': rec.texto,
            'mascota_id': rec.mascota_id
        })
    return jsonify(resultado)
