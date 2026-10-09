import sqlite3
from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Clave secreta para firmar las cookies de sesión
app.secret_key = 'super_secret_key_dev'
DB_NAME = 'database.db'

def init_db():
    """Inicializa la base de datos SQLite y la tabla de usuarios."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('contraseña')

    if not usuario or not password:
        return jsonify({"error": "Faltan datos obligatorios (usuario y contraseña)"}), 400

    # Hash de la contraseña antes de guardarla
    hashed_password = generate_password_hash(password)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, password) VALUES (?, ?)", 
                           (usuario, hashed_password))
            conn.commit()
        return jsonify({"mensaje": f"Usuario '{usuario}' registrado con éxito."}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El usuario ya existe en la base de datos."}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    password = data.get('contraseña')

    if not usuario or not password:
        return jsonify({"error": "Faltan credenciales"}), 400

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE usuario = ?", (usuario,))
        user_record = cursor.fetchone()

    # Verificar que el usuario exista y que el hash coincida con la contraseña ingresada
    if user_record and check_password_hash(user_record[0], password):
        session['logged_in'] = True
        session['usuario'] = usuario
        return jsonify({"mensaje": "Inicio de sesión exitoso. Tienes acceso a las tareas."}), 200
    else:
        return jsonify({"error": "Credenciales inválidas."}), 401

@app.route('/tareas', methods=['GET'])
def tareas():
    # validación de la sesión
    if not session.get('logged_in'):
        return jsonify({"error": "No autorizado. Inicie sesión primero."}), 401
    
    usuario = session.get('usuario')
    # HTML de bienvenida
    html_response = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><title>Mis Tareas</title></head>
    <body>
        <h1>¡Bienvenido a tu panel de tareas, {usuario}!</h1>
        <p>Aquí verás tus tareas pendientes.</p>
    </body>
    </html>
    """
    return html_response, 200

if __name__ == '__main__':
    init_db()
   
    app.run(debug=True, port=5000)