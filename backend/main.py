import logging
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_apscheduler import APScheduler
from flask_cors import CORS
from dotenv import load_dotenv
import os
import datetime
import easyocr
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import pymongo

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MONGO_URI'] = "mongodb+srv://parminder13dev:qFkk7C0jXQifQglj@checkdata.7twp6.mongodb.net/?retryWrites=true&w=majority"

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# MongoDB connection using pymongo directly
try:
    client = pymongo.MongoClient(app.config['MONGO_URI'])
    # Attempt to retrieve server information
    server_info = client.server_info()
    print("Connected to MongoDB successfully!")
    print("Server information:", server_info)
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # Initialize for English

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_image(image_path, languages=['en']):
    try:
        image = Image.open(image_path)
        image_np = np.array(image)
        results = reader.readtext(image_np)
        extracted_text = ' '.join([result[1] for result in results])
        return extracted_text
    except Exception as e:
        logger.exception(f"Error during text extraction: {e}")
        return ""

@app.route('/api/upload', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type', 'Authorization'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract text from image
        product_name = extract_text_from_image(file_path, languages=['en'])

        # Store file information in MongoDB
        file_info = {
            "filename": filename,
            "path": file_path,
            "upload_date": datetime.datetime.utcnow(),
            "product_name": product_name
        }

        # Insert the file information into MongoDB
        result = client.db.files.insert_one(file_info)

        if result.inserted_id:
            return jsonify({
                "message": "File uploaded successfully and processed",
                "path": file_path,
                "extracted_text": product_name,
                "file_id": str(result.inserted_id)
            }), 200
        else:
            return jsonify({"error": "Failed to store file information in MongoDB"}), 500
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/api/getinventory', methods=['GET'])
def get_inventory():
    try:
        # Use find() to retrieve documents
        cursor = client.db.inventory_items.find({}, {'_id': 0})
        items = list(cursor)

        if not items:
            return jsonify({"message": "Inventory is empty"}), 200

        return jsonify(items), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve inventory"}), 500

@app.route('/api/inventory/<name>', methods=['PUT'])
def update_inventory_item(name):
    data = request.get_json()
    quantity = data.get('quantity')

    if quantity is not None:
        try:
            result = client.db.inventory_items.update_one({'name': name}, {'$set': {'quantity': quantity}})
            if result.modified_count:
                return jsonify({"msg": "Item updated successfully"}), 200
            else:
                return jsonify({"error": "Item not found"}), 404
        except Exception as e:
            return jsonify({"error": "Failed to update item"}), 500
    return jsonify({"error": "Quantity is required"}), 400

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    try:
        low_stock_items = list(client.db.inventory_items.find({"quantity": {"$lt": 10}}, {'_id': 0}))
        return jsonify(low_stock_items), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve alerts"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
