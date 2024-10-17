import os
import json
import sqlite3
import numpy as np
from skimage.metrics import mean_squared_error
from difflib import SequenceMatcher
from flask import Flask, request, jsonify
import asyncio
import websockets
import subprocess
from threading import Thread
from neo_lux import QuantumIntelligence

# Define the path to the file-based storage for the HybridDatabase
DATA_FILE_PATH = 'data_store.json'

# Hybrid Database class for key-value store with file persistence
class HybridDatabase:
    def __init__(self):
        # Initialize the in-memory store and load from file
        self.memory_store = {}
        self.load_data()

    def load_data(self):
        """Load data from file if it exists."""
        if os.path.exists(DATA_FILE_PATH):
            with open(DATA_FILE_PATH, 'r') as file:
                self.memory_store = json.load(file)
        else:
            self.memory_store = {}

    def save_data(self):
        """Save data to file."""
        with open(DATA_FILE_PATH, 'w') as file:
            json.dump(self.memory_store, file)

    def insert_data(self, key, value):
        """Insert data into the in-memory store and save to file."""
        self.memory_store[key] = value
        self.save_data()
        return "Data successfully processed and stored."

    def query_data(self, key):
        """Query data from the in-memory store."""
        return self.memory_store.get(key, "No data found.")

# Initialize the HybridDatabase instance
db = HybridDatabase()

# Flask application setup
app = Flask(__name__)

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        if 'key' in data and 'value' in data:
            result = db.insert_data(data['key'], data['value'])
            return jsonify({'status': 'success', 'message': result}), 201
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    else:
        # Return all data stored in memory for simplicity
        return jsonify(db.memory_store), 200

# WebSocket server setup
async def handle_client(websocket, path):
    async for message in websocket:
        print(f"Received data from client: {message}")
        
        # Parse the received message
        data = json.loads(message)
        
        # Ensure data contains the key and value
        if 'key' in data and 'value' in data:
            result = db.insert_data(data['key'], data['value'])
        elif 'key' in data:
            result = db.query_data(data['key'])
        else:
            result = "Invalid data format."
        
        # Send the result back to the client
        await websocket.send(result)

# WebSocket server start function
async def start_websocket_server():
    start_server = websockets.serve(handle_client, "localhost", 5000)
    await start_server

# Flask and WebSocket server runner
def run_flask_app():
    app.run(port=5001, debug=True, use_reloader=False)

# Dynamic Local Virtual Database for managing SQLite operations
class DynamicLocalVirtualDatabase:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_table(self, table_name, columns):
        columns_with_types = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})")
        self.connection.commit()

    def insert_data(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        values = tuple(data.values())
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.connection.commit()

    def query_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_data(self, table_name, updates, condition):
        update_str = ', '.join([f"{col} = ?" for col in updates.keys()])
        values = tuple(updates.values())
        self.cursor.execute(f"UPDATE {table_name} SET {update_str} WHERE {condition}", values)
        self.connection.commit()

    def delete_data(self, table_name, condition):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.connection.commit()

    def close(self):
        self.connection.close()

# Integrated system combining the SQLite database and QuantumIntelligence predictions
class IntegratedSystem:
    def __init__(self, db_path):
        self.dlvd = DynamicLocalVirtualDatabase(db_path)
        self.qi = QuantumIntelligence()

    def update_and_predict(self, table_name, query):
        data = self.dlvd.query_data(query)
        predictions = []
        for row in data:
            # Adjust row to match QuantumIntelligence input requirements
            formatted_data = np.array(row)
            prediction = self.qi.make_decision(formatted_data.tolist())
            predictions.append((row, prediction))
        return predictions

    def add_data_and_predict(self, table_name, data):
        self.dlvd.insert_data(table_name, data)
        predictions = self.update_and_predict(table_name, f"SELECT * FROM {table_name}")
        return predictions

# Flask route to interact with the integrated system
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

# Background task to run WebSocket server
def run_websocket_server():
    asyncio.run(start_websocket_server())

# Threading to run both Flask and WebSocket servers simultaneously
if __name__ == '__main__':
    # Initialize integrated system with SQLite DB
    db_path = 'virtual_database.db'
    integrated_system = IntegratedSystem(db_path)

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Run WebSocket server in the main thread
    run_websocket_server()
