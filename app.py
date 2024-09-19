from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy como ORM para manejar la base de datos
db = SQLAlchemy(app)

# Definición del modelo Tareas
class Tareas(db.Model):
    """
    Modelo de la tabla 'Tareas' en la base de datos.
    Representa una tarea con un título, descripción, fecha de creación y estado (hecho o no).
    """
    id = db.Column(db.Integer, primary_key=True)  # Identificador único de la tarea
    titulo = db.Column(db.String(120), nullable=False)  # Título de la tarea
    descripcion = db.Column(db.String(500), nullable=True)  # Descripción opcional de la tarea
    creado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Fecha de creación, por defecto es la fecha y hora actual
    hecho = db.Column(db.Boolean, default=False)  # Estado de la tarea, si está completada o no

# Crear la tabla 'Tareas' si no existe
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    Renderiza la página principal.
    
    Retorna:
        HTML: Página principal que lista todas las tareas.
    """
    return render_template('index.html')

@app.route('/crear_tarea')
def crear_tarea():
    """
    Renderiza la página de creación de tareas.
    
    Retorna:
        HTML: Página para crear una nueva tarea.
    """
    return render_template('crear_tareas.html')

@app.route('/api/tareas', methods=['GET'])
def get_todas_las_tareas():
    """
    Retorna todas las tareas almacenadas en la base de datos en formato JSON.
    
    Retorna:
        JSON: Lista de tareas con sus propiedades (id, título, descripción, fecha de creación, estado).
    """
    tareas = Tareas.query.all()  # Obtener todas las tareas de la base de datos
    return jsonify([{
        'id': tarea.id,
        'titulo': tarea.titulo,
        'descripcion': tarea.descripcion,
        'creado': tarea.creado.isoformat(),  # Convertir fecha a formato ISO 8601
        'hecho': tarea.hecho
    } for tarea in tareas])

@app.route('/api/tareas', methods=['POST'])
def add_tarea():
    """
    Agrega una nueva tarea a la base de datos.
    
    Requiere:
        JSON con 'titulo' y opcionalmente 'descripcion'.
    
    Retorna:
        JSON: Datos de la tarea recién creada (id, título, descripción, fecha de creación).
    """
    data = request.json  # Obtener los datos JSON enviados en la solicitud
    new_tarea = Tareas(
        titulo=data['titulo'],
        descripcion=data.get('descripcion')  # Descripción es opcional
    )
    db.session.add(new_tarea)  # Agregar nueva tarea a la sesión de la base de datos
    db.session.commit()  # Confirmar los cambios

    return jsonify({
        'id': new_tarea.id,
        'titulo': new_tarea.titulo,
        'descripcion': new_tarea.descripcion,
        'creado': new_tarea.creado.isoformat()
    })

@app.route('/api/tareas/<int:tarea_id>', methods=['PUT'])
def update_tarea(tarea_id):
    """
    Actualiza una tarea existente basada en su ID.
    
    Parámetros:
        tarea_id (int): El ID de la tarea a actualizar.
    
    Requiere:
        JSON con los campos a actualizar ('titulo', 'descripcion', 'hecho').
    
    Retorna:
        JSON: Datos de la tarea actualizada o un mensaje de error si no se encuentra.
    """
    tarea = Tareas.query.get(tarea_id)  # Obtener la tarea por su ID
    if tarea:
        data = request.json  # Obtener datos JSON enviados en la solicitud
        tarea.titulo = data.get('titulo', tarea.titulo)  # Actualizar título si se proporciona
        tarea.descripcion = data.get('descripcion', tarea.descripcion)  # Actualizar descripción si se proporciona
        tarea.hecho = data.get('hecho', tarea.hecho)  # Actualizar estado si se proporciona
        db.session.commit()  # Confirmar los cambios
        return jsonify({
            'id': tarea.id,
            'titulo': tarea.titulo,
            'descripcion': tarea.descripcion,
            'creado': tarea.creado.isoformat(),
            'hecho': tarea.hecho
        })
    return jsonify({'message': 'Tarea no encontrada'}), 404  # Retornar mensaje de error si la tarea no existe

@app.route('/api/tareas/<int:tarea_id>', methods=['DELETE'])
def delete_tarea(tarea_id):
    """
    Elimina una tarea existente basada en su ID.
    
    Parámetros:
        tarea_id (int): El ID de la tarea a eliminar.
    
    Retorna:
        JSON: Mensaje de confirmación o de error si no se encuentra la tarea.
    """
    tarea = Tareas.query.get(tarea_id)  # Obtener la tarea por su ID
    if tarea:
        db.session.delete(tarea)  # Eliminar la tarea de la base de datos
        db.session.commit()  # Confirmar los cambios
        return jsonify({'message': 'Tarea eliminada'})
    return jsonify({'message': 'Tarea no encontrada'}), 404  # Retornar mensaje de error si la tarea no existe

if __name__ == '__main__':
    app.run(debug=True)
