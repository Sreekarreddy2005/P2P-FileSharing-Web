#Iports and setup
#import flask for web frameworks and SocketIO for real-time communication, os for file operations, and uuid for generating unique file names.
from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit
import os
import uuid
# Initialize SocketIO for handling WebSocket connections.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
#File upload directory
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
#Render the index.html template when the root URL is accessed.
@app.route('/')
def index():
    return render_template('index.html')
  
#Handle file uploads. Save the uploaded file with a unique name and return a URL for downloading the file.
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    file_url = request.host_url + 'download/' + filename
    return {'file_url': file_url}

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
  
#Emit a message when a client connects to the WebSocket.
@socketio.on('connect')
def handle_connect():
    emit('message', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
