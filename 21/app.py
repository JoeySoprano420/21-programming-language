import os
import json
import sqlite3
import numpy as np
import asyncio
from flask import Flask, request, jsonify
from threading import Thread
from your_quantum_intelligence_module import QuantumIntelligence  # Import your QuantumIntelligence implementation
from your_dynamic_database_module import DynamicLocalVirtualDatabase  # Import your SQLite interface

app = Flask(__name__)

# Define the path to the file-based storage for the HybridDatabase
DATA_FILE_PATH = 'data_store.json'

class HybridDatabase:
    def __init__(self):
        self.memory = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE_PATH):
            with open(DATA_FILE_PATH, 'r') as f:
                self.memory = json.load(f)

    def save_data(self):
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump(self.memory, f)

    def insert_data(self, key, value):
        self.memory[key] = value
        self.save_data()
        return f"Data inserted: {key} -> {value}"

    def query_data(self, key):
        return self.memory.get(key, "No data found.")

class IntegratedSystem:
    def __init__(self, db_path):
        self.dlvd = DynamicLocalVirtualDatabase(db_path)
        self.qi = QuantumIntelligence()

    def update_and_predict(self, table_name, query):
        data = self.dlvd.query_data(query)
        predictions = []
        for row in data:
            formatted_data = np.array(row)
            prediction = self.qi.make_decision(formatted_data.tolist())
            predictions.append((row, prediction))
        return predictions

    def add_data_and_predict(self, table_name, data):
        self.dlvd.insert_data(table_name, data)
        predictions = self.update_and_predict(table_name, f"SELECT * FROM {table_name}")
        return predictions

# Initialize integrated system with SQLite DB
db_path = 'virtual_database.db'
integrated_system = IntegratedSystem(db_path)

@app.route('/api/data', methods=['POST'])
def insert_data():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    message = db.insert_data(key, value)
    return jsonify({"message": message})

@app.route('/api/data', methods=['GET'])
def query_data():
    key = request.args.get('key')
    value = db.query_data(key)
    return jsonify({key: value})

@app.route('/api/predict', methods=['POST'])
def handle_predict():
    data = request.json
    if 'table' in data and 'query' in data:
        try:
            predictions = integrated_system.update_and_predict(data['table'], data['query'])
            return jsonify({'status': 'success', 'predictions': predictions}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'error', 'message': 'Invalid request format'}), 400

def run_flask_app():
    app.run(debug=True, use_reloader=False)

# Background task to run WebSocket server
async def start_websocket_server():
    async with websockets.serve(your_websocket_handler, 'localhost', 8765):
        await asyncio.Future()  # Run forever

def run_websocket_server():
    asyncio.run(start_websocket_server())

if __name__ == '__main__':
    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Run WebSocket server in the main thread
    run_websocket_server()
