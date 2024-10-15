# Unified ML-Plus Program

import os
import json
import asyncio
import websockets
from flask import Flask, request, jsonify
from threading import Thread
import tkinter as tk
from tkinter import messagebox
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import mean_squared_error
from difflib import SequenceMatcher

# --------------------- 1. HybridDatabase (JSON-based File Storage) --------------------- 
DATA_FILE_PATH = 'data_store.json'

class HybridDatabase:
    def __init__(self):
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


# --------------------- 2. MLPlusAlgorithm (Machine Learning-Like Deductive Engine) --------------------- 
class MLPlusAlgorithm:
    def __init__(self):
        self.knowledge_base = {}
        self.model_registry = {
            'RandomForest': RandomForestClassifier(),
            'SVM': SVC()
        }

    def learn(self, example, classification):
        """Add examples to the knowledge base."""
        if example not in self.knowledge_base:
            self.knowledge_base[example] = classification

    def classify(self, input_example):
        """Classify an input example using deductive reasoning."""
        if input_example in self.knowledge_base:
            return self.knowledge_base[input_example]

        for example, classification in self.knowledge_base.items():
            if self.is_similar(input_example, example):
                return classification

        return "Unknown"

    def is_similar(self, example1, example2):
        """Implement similarity comparison logic between two examples."""
        return self.is_text_similar(example1, example2)

    def is_text_similar(self, text1, text2):
        """Compare text for similarity using SequenceMatcher (edit distance)."""
        similarity_ratio = SequenceMatcher(None, text1, text2).ratio()
        return similarity_ratio > 0.8

    def fit_model(self, model_name, X, y):
        """Fit the specified machine learning model."""
        model = self.model_registry.get(model_name)
        if model:
            model.fit(X, y)
            return "Model trained successfully."
        return "Model not found."

    def predict(self, model_name, X):
        """Make predictions using the specified machine learning model."""
        model = self.model_registry.get(model_name)
        if model:
            return model.predict(X)
        return "Model not found."


# --------------------- 3. Flask REST API --------------------- 
app = Flask(__name__)
db = HybridDatabase()
ml_algorithm = MLPlusAlgorithm()

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        if 'key' in data and 'value' in data:
            result = db.insert_data(data['key'], data['value'])
            return jsonify({'status': 'success', 'message': result}), 201
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    else:
        return jsonify(db.memory_store), 200

@app.route('/api/model/train', methods=['POST'])
def train_model():
    data = request.json
    model_name = data.get('model_name')
    X = np.array(data.get('X'))  # Assuming X is a list of lists
    y = np.array(data.get('y'))   # Assuming y is a list
    result = ml_algorithm.fit_model(model_name, X, y)
    return jsonify({'status': 'success', 'message': result}), 200

@app.route('/api/model/predict', methods=['POST'])
def predict():
    data = request.json
    model_name = data.get('model_name')
    X = np.array(data.get('X'))  # Assuming X is a list of lists
    predictions = ml_algorithm.predict(model_name, X)
    return jsonify({'predictions': predictions.tolist()}), 200


# --------------------- 4. WebSocket Server --------------------- 
async def handle_client(websocket, path):
    async for message in websocket:
        print(f"Received data from client: {message}")
        data = json.loads(message)

        if 'key' in data and 'value' in data:
            result = db.insert_data(data['key'], data['value'])
        elif 'key' in data:
            result = db.query_data(data['key'])
        else:
            result = "Invalid data format."

        await websocket.send(result)

async def start_websocket_server():
    start_server = websockets.serve(handle_client, "localhost", 5000)
    await start_server


def run_flask_app():
    app.run(port=5001, debug=True, use_reloader=False)


# --------------------- 5. Tkinter User Interface --------------------- 
class MLPlusApp:
    def __init__(self, master):
        self.master = master
        master.title("ML-Plus User Interface")

        # Create UI Components
        self.label = tk.Label(master, text="Enter Key:")
        self.label.pack()

        self.key_entry = tk.Entry(master)
        self.key_entry.pack()

        self.label_value = tk.Label(master, text="Enter Value:")
        self.label_value.pack()

        self.value_entry = tk.Entry(master)
        self.value_entry.pack()

        self.insert_button = tk.Button(master, text="Insert Data", command=self.insert_data)
        self.insert_button.pack()

        self.query_button = tk.Button(master, text="Query Data", command=self.query_data)
        self.query_button.pack()

        self.result_area = tk.Text(master, height=10, width=50)
        self.result_area.pack()

    def insert_data(self):
        key = self.key_entry.get()
        value = self.value_entry.get()
        result = db.insert_data(key, value)
        self.result_area.insert(tk.END, result + "\n")
        self.key_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)

    def query_data(self):
        key = self.key_entry.get()
        result = db.query_data(key)
        self.result_area.insert(tk.END, result + "\n")
        self.key_entry.delete(0, tk.END)


if __name__ == '__main__':
    websocket_thread = Thread(target=lambda: asyncio.run(start_websocket_server()))
    websocket_thread.start()
    
    # Start the Flask app in a separate thread
    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()

    # Start the Tkinter application
    root = tk.Tk()
    app = MLPlusApp(root)
    root.mainloop()
