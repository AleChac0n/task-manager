from flask import Flask, request, jsonify, render_template
import pyodbc


app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks-page')
def tasks_page():
    try:
        cursor.execute("SELECT id, title, description, status FROM Tasks")
        tasks = cursor.fetchall()
        if not tasks:
            print("No hay tareas en la base de datos.")
        return render_template('tasks.html', tasks=tasks)
    except Exception as e:
        print("Error al obtener tareas:", e)
        return "Error al cargar las tareas", 500

# Configuración de la conexión a SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=Alejandro\\MSSQLSERVER01;'
    'DATABASE=TaskManager;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()



@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    cursor.execute(
        "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
        (data['username'], data['email'], data['password_hash'])
    )
    conn.commit()
    return jsonify({"message": "Usuario creado"}), 201  

@app.route('/users', methods=['GET'])
def get_users():
    cursor.execute("SELECT id, username, email FROM Users")
    users = cursor.fetchall()
    return jsonify([{
        "id": row[0],
        "username": row[1],
        "email": row[2]
    } for row in users]), 200
    
@app.route('/task', methods=['POST'])
def create_task():
    data = request.get_json()  # Obtener datos en formato JSON
    try:
        cursor.execute(
            "INSERT INTO Tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)",
            (data['title'], data['description'], data.get('status', 'Pending'), data['user_id'])
        )
        conn.commit()
        return jsonify({"message": "Tarea creada", "task": data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Devolver un error si algo falla


@app.route('/tasks/<int:user_id>', methods=['GET'])
def get_tasks(user_id):
    cursor.execute("SELECT id, title, description, status FROM Tasks WHERE user_id = ?", user_id)
    tasks = cursor.fetchall()
    return jsonify([{
        "id": row[0],
        "title": row[1],
        "description": row[2],
        "status": row[3]
    } for row in tasks]), 200
    
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    data = request.get_json()
    cursor.execute(
        "UPDATE Tasks SET status = ? WHERE id = ?",
        (data['status'], task_id)
    )
    conn.commit()
    return jsonify({"message": "Estado de la tarea actualizado"}), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor.execute("DELETE FROM Tasks WHERE id = ?", task_id)
    conn.commit()
    return jsonify({"message": "Tarea eliminada"}), 200

if __name__ == "__main__":
    app.run(debug=True)
