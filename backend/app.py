from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from ai_module.album_creation import create_photo_albums
from PIL import Image
import logging

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
ALBUM_FOLDER = 'albums'
THUMBNAIL_FOLDER = 'thumbnails'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALBUM_FOLDER'] = ALBUM_FOLDER
app.config['THUMBNAIL_FOLDER'] = THUMBNAIL_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(ALBUM_FOLDER):
    os.makedirs(ALBUM_FOLDER)
if not os.path.exists(THUMBNAIL_FOLDER):
    os.makedirs(THUMBNAIL_FOLDER)

logging.basicConfig(level=logging.INFO)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'images' not in request.files:
        return jsonify({'error': 'No files part in the request'}), 400

    files = request.files.getlist('images')
    file_paths = []
    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        file_paths.append(file_path)
        logging.info(f"Uploaded file: {file_path}")

    try:
        album_paths = create_photo_albums(file_paths, ALBUM_FOLDER)
        album_urls = [f"http://localhost:5000/albums/{os.path.basename(path)}" for path in album_paths]
        return jsonify({'albumUrls': album_urls})
    except Exception as e:
        logging.error(f"Error creating albums: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/albums/<filename>', methods=['GET'])
def get_album(filename):
    return send_from_directory(app.config['ALBUM_FOLDER'], filename, as_attachment=True)

def create_thumbnail(image_path, thumbnail_folder):
    try:
        with Image.open(image_path) as img:
            img.thumbnail((128, 128))
            base, ext = os.path.splitext(os.path.basename(image_path))
            thumbnail_path = os.path.join(thumbnail_folder, f"{base}_thumbnail{ext}")
            img.save(thumbnail_path, "JPEG")
            logging.info(f"Created thumbnail: {thumbnail_path}")
            return thumbnail_path
    except Exception as e:
        logging.error(f"Error creating thumbnail for {image_path}: {e}")
        return None

@app.route('/thumbnail/<filename>', methods=['GET'])
def get_thumbnail(filename):
    album_path = os.path.join(app.config['ALBUM_FOLDER'], filename)
    if album_path.endswith('.pdf'):
        return jsonify({'error': 'Thumbnails are not supported for PDF files'}), 400

    thumbnail_path = create_thumbnail(album_path, app.config['THUMBNAIL_FOLDER'])
    if thumbnail_path:
        return send_from_directory(app.config['THUMBNAIL_FOLDER'], os.path.basename(thumbnail_path))
    else:
        return jsonify({'error': 'Thumbnail creation failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
