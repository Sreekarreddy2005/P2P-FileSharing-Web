import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename

# Configure the Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for session management

UPLOAD_FOLDER = 'uploads'  # Directory to store uploaded files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}  # Allowed file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

USER_FILE = 'users.json'  # File to store user data

# Helper function to check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load users from file
def load_users():
    try:
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save users to file
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

# Initialize users
users = load_users()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# File upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    
    files = request.files.getlist('file')
    uploaded_file_urls = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded_file_urls.append(url_for('uploaded_file', filename=filename, _external=True))
    
    if uploaded_file_urls:
        return jsonify({'file_urls': uploaded_file_urls})
    else:
        return jsonify({'error': 'No valid files uploaded'}), 400

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        
        if email in users and users[email] == password:
            session['logged_in'] = True
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        
        if email in users:
            return jsonify({'error': 'User already exists'}), 400
        
        users[email] = password
        save_users(users)  # Save updated user data
        return jsonify({'success': True})
    
    return render_template('register.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# Session status route to check if user is logged in
@app.route('/session-status')
def session_status():
    return jsonify({'logged_in': 'logged_in' in session})

# Static route to serve CSS, JS, and images
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
