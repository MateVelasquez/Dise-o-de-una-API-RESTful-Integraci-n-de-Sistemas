from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenamiento temporal de tareas
tasks = []
task_id_counter = 1

# Función para insertar datos quemados
def insert_mock_data():
    global task_id_counter
    mock_tasks = [
        {"title": "Lavar el coche", "description": "Usar jabón especial", "status": "pendiente"},
        {"title": "Comprar comida", "description": "Comprar frutas y verduras", "status": "en progreso"},
        {"title": "Leer un libro", "description": "Terminar '1984' de George Orwell", "status": "completada"},
        {"title": "Hacer ejercicio", "description": "30 minutos de cardio", "status": "pendiente"},
        {"title": "Llamar al doctor", "description": "Confirmar cita médica", "status": "en progreso"}
    ]
    for task in mock_tasks:
        task['id'] = task_id_counter
        tasks.append(task)
        task_id_counter += 1

# Endpoint: Listar todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# Endpoint: Obtener una tarea específica
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({'error': 'Tarea no encontrada'}), 404

# Endpoint: Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.json
    if not data.get('title') or not data.get('status'):
        return jsonify({'error': 'Datos incompletos'}), 400
    new_task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'status': data['status']
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

# Endpoint: Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    data = request.json
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    task.update({
        'title': data.get('title', task['title']),
        'description': data.get('description', task['description']),
        'status': data.get('status', task['status'])
    })
    return jsonify(task), 200

# Endpoint: Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Tarea eliminada'}), 200

# Ejecutar la aplicación
if __name__ == '__main__':
    insert_mock_data()  # Insertar datos quemados al iniciar la aplicación
    app.run(debug=True)