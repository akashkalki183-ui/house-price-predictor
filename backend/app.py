# app.py
# This is your backend server

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Load the trained model
print("📦 Loading trained model...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

model = pickle.load(open(MODEL_PATH, 'rb'))

print("✅ Model loaded!")

# Database functions
def get_db():
    """Connect to database"""
    conn = sqlite3.connect('predictions.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database (create table if doesn't exist)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            square_feet INTEGER,
            bedrooms INTEGER,
            bathrooms REAL,
            predicted_price REAL,
            date_created TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized!")

# Initialize database when app starts
init_db()

# ====================
# ROUTES (Endpoints)
# ====================

@app.route('/', methods=['GET'])
def home():
    """Welcome message"""
    return jsonify({
        'message': '🏠 House Price Predictor API is running!',
        'version': '1.0',
        'endpoints': {
            'predict': '/predict (POST)',
            'history': '/history (GET)',
            'clear_history': '/clear_history (DELETE)'
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives house data, predicts price, saves to database
    
    Expected JSON:
    {
        "square_feet": 2000,
        "bedrooms": 3,
        "bathrooms": 2
    }
    """
    try:
        # Get data from frontend
        data = request.json
        square_feet = float(data.get('square_feet'))
        bedrooms = int(data.get('bedrooms'))
        bathrooms = float(data.get('bathrooms'))
        
        # Validate input
        if square_feet <= 0 or bedrooms <= 0 or bathrooms <= 0:
            return jsonify({'error': 'All values must be positive numbers'}), 400
        
        if square_feet > 100000 or bedrooms > 20:
            return jsonify({'error': 'Invalid input values'}), 400
        
        # Make prediction
        prediction = model.predict([[square_feet, bedrooms, bathrooms]])[0]
        
        # Save to database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO predictions 
            (square_feet, bedrooms, bathrooms, predicted_price, date_created)
            VALUES (?, ?, ?, ?, ?)
        ''', (square_feet, bedrooms, bathrooms, prediction, datetime.now()))
        conn.commit()
        conn.close()
        
        # Return prediction
        return jsonify({
            'success': True,
            'predicted_price': round(prediction, 2),
            'input': {
                'square_feet': square_feet,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms
            }
        })
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def history():
    """Get all past predictions"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM predictions ORDER BY date_created DESC')
        rows = cursor.fetchall()
        conn.close()
        
        predictions = []
        for row in rows:
            predictions.append({
                'id': row['id'],
                'square_feet': row['square_feet'],
                'bedrooms': row['bedrooms'],
                'bathrooms': row['bathrooms'],
                'predicted_price': row['predicted_price'],
                'date': row['date_created']
            })
        
        return jsonify({
            'success': True,
            'count': len(predictions),
            'predictions': predictions
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clear_history', methods=['DELETE'])
def clear_history():
    """Clear all predictions from database"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM predictions')
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Prediction history cleared'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

# ====================
# RUN SERVER
# ====================

if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 STARTING FLASK SERVER")
    print("=" * 50)
    print("\n📍 Server running at: http://localhost:5000")
    print("📍 API Documentation: http://localhost:5000/")
    print("\n⚠️  Press CTRL+C to stop the server\n")
    print("=" * 50 + "\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')