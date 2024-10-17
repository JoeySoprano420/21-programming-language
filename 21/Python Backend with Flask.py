import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the path to the file-based storage for the HybridDatabase
DATA_FILE_PATH = 'data_store.json'

class HybridDatabase:
    def __init__(self):
        # Initialize the in-memory store and load from file
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

db = HybridDatabase()

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

if __name__ == "__main__":
    app.run(debug=True)
