from flask import Flask, render_template, request, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import os
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from flask_socketio import SocketIO, emit
import os
import uuid
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dummy user data for demonstration purposes
users = {}

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if email in users and users[email] == password:
            response = make_response(jsonify({'success': True}))
            response.set_cookie('loggedIn', 'true', max_age=60*60*24*30)  # Cookie expires in 30 days
            return response
        else:
            return jsonify({'error': 'Invalid email or password.'})
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Email validation regex
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        # Password validation regex (at least one capital letter, one symbol, and minimum length of 8)
        password_regex = r'^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9]).{8,}$'

        if not re.match(email_regex, email):
            return jsonify({'error': 'Invalid email format.'})

        if not re.match(password_regex, password):
            return jsonify({'error': 'Password must contain at least one capital letter, one symbol, and be at least 8 characters long.'})

        if email in users:
            return jsonify({'error': 'Email is already registered. <a href="/login">Go to Login</a>'})

        users[email] = password
        return jsonify({'success': True})
    return render_template('register.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        file_url = request.host_url + 'download/' + filename
        return jsonify({'file_url': file_url, 'message': 'File uploaded successfully!'})
    except Exception as e:
        return jsonify({'error': 'File upload failed. Please try again.'}), 500

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    file_url = request.host_url + 'download/' + filename
    return jsonify({'file_url': file_url, 'message': 'File uploaded successfully!'})

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
