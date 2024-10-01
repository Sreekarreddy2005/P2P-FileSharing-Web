import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_from_directory
from werkzeug.utils import secure_filename
import qrcode  # Importing the qrcode library

# Configure the Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  #16MB max-limit
USER_FILE = 'users.csv'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_users():
    try:
        return pd.read_csv(USER_FILE, index_col='email').to_dict()['password']
    except FileNotFoundError:
        return {}

def save_users(users):
    df = pd.DataFrame(list(users.items()), columns=['email', 'password'])
    df.to_csv(USER_FILE, index=False)

users = load_users()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400
    
    files = request.files.getlist('file')
    if not files:
        return jsonify({'error': 'No files provided'}), 400

    uploaded_file_urls = []
    qr_codes = []  # List to hold QR code URLs
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_url = url_for('uploaded_file', filename=filename, _external=True)
                uploaded_file_urls.append(file_url)
                
                # Generate QR code for the file URL
                qr_code_img_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{filename}.png")
                qr_code_img = qrcode.make(file_url)
                qr_code_img.save(qr_code_img_path)
                qr_codes.append(url_for('uploaded_qr_code', filename=f"{filename}.png", _external=True))
                
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        else:
            return jsonify({'error': f'File {file.filename} is not allowed'}), 400

    if uploaded_file_urls:
        return jsonify({'file_urls': uploaded_file_urls, 'qr_codes': qr_codes})
    else:
        return jsonify({'error': 'No valid files uploaded'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/qrcodes/<filename>')
def uploaded_qr_code(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        
        if email in users and users[email] == password:
            session['logged_in'] = True
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        
        if email in users:
            return jsonify({'error': 'User already exists'}), 400
        
        users[email] = password
        save_users(users)
        return jsonify({'success': True})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/session-status')
def session_status():
    return jsonify({'logged_in': 'logged_in' in session})

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
