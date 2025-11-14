
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from database import db

cuidador_bp = Blueprint('cuidador', __name__)

class Cuidador(db.Model):
    __tablename__ = 'cuidador'
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20))
    rol = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    foto_perfil = db.Column(db.Text)


# Crear cuidador
@cuidador_bp.route('/cuidadores', methods=['POST'])
def crear_cuidador():
    data = request.json
    nuevo = Cuidador(**data)
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'mensaje': 'Cuidador creado', 'id': nuevo.id}), 201

# Obtener cuidador por ID
@cuidador_bp.route('/cuidadores/<int:id>', methods=['GET'])
def obtener_cuidador(id):
    cuidador = Cuidador.query.get_or_404(id)
    return jsonify({
        'id': cuidador.id,
        'nombre_completo': cuidador.nombre_completo,
        'correo': cuidador.correo,
        'telefono': cuidador.telefono,
        'rol': cuidador.rol,
        'direccion': cuidador.direccion,
        'foto_perfil': cuidador.foto_perfil
    })

# Actualizar cuidador
@cuidador_bp.route('/cuidadores/<int:id>', methods=['PUT'])
def actualizar_cuidador(id):
    cuidador = Cuidador.query.get_or_404(id)
    data = request.json
    for campo, valor in data.items():
        setattr(cuidador, campo, valor)
    db.session.commit()
    return jsonify({'mensaje': 'Cuidador actualizado'})

# Eliminar cuidador
@cuidador_bp.route('/cuidadores/<int:id>', methods=['DELETE'])
def eliminar_cuidador(id):
    cuidador = Cuidador.query.get_or_404(id)
    db.session.delete(cuidador)
    db.session.commit()
    return jsonify({'mensaje': 'Cuidador eliminado'})

# Obtener todos los cuidadores
@cuidador_bp.route('/cuidadores', methods=['GET'])
def obtener_cuidadores():
    cuidadores = Cuidador.query.all()
    resultado = []
    for c in cuidadores:
        resultado.append({
            'id': c.id,
            'nombre_completo': c.nombre_completo,
            'correo': c.correo,
            'telefono': c.telefono,
            'rol': c.rol,
            'direccion': c.direccion,
            'foto_perfil': c.foto_perfil
        })
    return jsonify(resultado)


@cuidador_bp.route('/login', methods=['POST'])
def login_cuidador():
    data = request.json
    correo = data.get('correo', '').strip()
    contrasena = data.get('contrasena', '').strip()

    cuidador = Cuidador.query.filter_by(correo=correo, contrasena=contrasena).first()
    if cuidador:
        return jsonify({
            'id': cuidador.id,
            'nombre_completo': cuidador.nombre_completo,
            'correo': cuidador.correo,
            'telefono': cuidador.telefono,
            'rol': cuidador.rol,
            'direccion': cuidador.direccion,
            'foto_perfil': cuidador.foto_perfil
        })
    else:
        return jsonify({'error': 'Credenciales incorrectas'}), 401
