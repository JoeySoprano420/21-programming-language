import os
import json
import asyncio
import websockets
from flask import Flask, request, jsonify
from threading import Thread
from skimage.metrics import mean_squared_error
from difflib import SequenceMatcher
import re

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


# --------------------- 2. Flask REST API ---------------------
db = HybridDatabase()
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
        return jsonify(db.memory_store), 200


# --------------------- 3. WebSocket Server ---------------------
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

if __name__ == '__main__':
    websocket_thread = Thread(target=lambda: asyncio.run(start_websocket_server()))
    websocket_thread.start()
    run_flask_app()


# --------------------- 4. MLPlusAlgorithm (Machine Learning-Like Deductive Engine) ---------------------
class MLPlusAlgorithm:
    def __init__(self):
        self.knowledge_base = {}

    def learn(self, example, classification):
        """Add examples to the knowledge base."""
        if example not in self.knowledge_base:
            self.knowledge_base[example] = classification

    def classify(self, input_example):
        """Classify an input example using deductive reasoning and process of elimination."""
        if input_example in self.knowledge_base:
            return self.knowledge_base[input_example]

        for example, classification in self.knowledge_base.items():
            if self.is_similar(input_example, example):
                return classification

        return "Unknown"

    def is_similar(self, example1, example2):
        """Implement similarity comparison logic between two examples."""
        return self.is_text_similar(example1, example2)

    def is_image_similar(self, img1, img2):
        """Compare images for similarity using Mean Squared Error (MSE)."""
        mse = mean_squared_error(img1, img2)
        return mse < 0.1

    def is_text_similar(self, text1, text2):
        """Compare text for similarity using SequenceMatcher (edit distance)."""
        similarity_ratio = SequenceMatcher(None, text1, text2).ratio()
        return similarity_ratio > 0.8


# --------------------- 5. Pseudocode-to-Python Translator ---------------------
# Regex-based pseudocode translator functions

def translate_function_def(match):
    name = match[1]
    params = match[2]
    body = match[3].strip().replace('\n', '\n    ')
    return f'def {name}({params}):\n    {body}'

def translate_function_call(match):
    name = match[1]
    args = match[2]
    return f'{name}({args})'

def translate_let_statement(match):
    var_name = match[1]
    value = match[2]
    value = handle_data_structures(value)
    return f'{var_name} = {value}'

def translate_for_loop(match):
    var_name = match[1]
    iterable = match[2]
    body = match[3].strip().replace('\n', '\n    ')
    return f'for {var_name} in {iterable}:\n    {body}'

def handle_data_structures(value):
    """Process and handle data structures."""
    return value

# Regex patterns for different pseudocode structures
function_def_pattern = re.compile(r'function (\w+)\((.*)\)\s*{([\s\S]*?)}')
function_call_pattern = re.compile(r'call (\w+)\((.*)\)')
let_statement_pattern = re.compile(r'let (\w+) = (.+)')
for_loop_pattern = re.compile(r'for (\w+) in (.+) {([\s\S]*?)}')

def translate_pseudocode(pseudocode):
    # Translating pseudocode into Python code
    pseudocode = function_def_pattern.sub(translate_function_def, pseudocode)
    pseudocode = function_call_pattern.sub(translate_function_call, pseudocode)
    pseudocode = let_statement_pattern.sub(translate_let_statement, pseudocode)
    pseudocode = for_loop_pattern.sub(translate_for_loop, pseudocode)
    return pseudocode

# Example pseudocode
pseudocode = """
function add(a, b) {
    let result = a + b
    return result
}
"""

translated_python_code = translate_pseudocode(pseudocode)
exec(translated_python_code)

import re

class _21Translator:
    def __init__(self):
        self.variables = {}

    def translate(self, _21code):
        """Main method to handle translation of 21-style pseudocode to Python."""
        # Translate variable declarations
        _21code = self.translate_var_declaration(_21code)
        # Translate arithmetic/assembly-style operations
        _21code = self.translate_arithmetic_operations(_21code)
        # Translate blackjack logic conditions
        _21code = self.translate_blackjack_logic(_21code)
        # Translate user prompts
        _21code = self.translate_user_prompts(_21code)
        # Translate mutation operations
        _21code = self.translate_mutation_operations(_21code)
        
        return _21code

    def translate_var_declaration(self, _21code):
        """Translates variable declarations."""
        pattern = re.compile(r"~\| var:(\w+) \[ (\w+) = (.+?) \] \|~")
        return pattern.sub(self._translate_variable_declaration, _21code)

    def _translate_variable_declaration(self, match):
        var_type, var_name, value = match.groups()
        if var_type == 'int':
            return f'{var_name} = {int(value)}'
        elif var_type == 'bool':
            return f'{var_name} = {value.lower() == "true"}'
        return f'{var_name} = {value}'

    def translate_arithmetic_operations(self, _21code):
        """Translates arithmetic or assembly-style operations."""
        pattern = re.compile(r"~\| eax <- (\d+) \|~")
        _21code = pattern.sub(lambda match: f'eax = {match[1]}', _21code)

        pattern = re.compile(r"~\| add eax, (\w+) \|~")
        _21code = pattern.sub(lambda match: f'eax += {match[1]}', _21code)

        pattern = re.compile(r"~\| store eax -> (\w+) \|~")
        _21code = pattern.sub(lambda match: f'{match[1]} = eax', _21code)

        pattern = re.compile(r"~\| (\w+) -> eax \* (\d+) \|~")
        return pattern.sub(lambda match: f'{match[1]} = eax * {match[2]}', _21code)

    def translate_blackjack_logic(self, _21code):
        """Translates blackjack-style logic blocks into Python if-elif statements."""
        pattern = re.compile(r"<IF:blackjack> (.+?) :IS: \[(.+?)\](.*?)@\| OUTPUT \"(.+?)\" \|@")
        _21code = pattern.sub(self._translate_blackjack_if, _21code)

        pattern = re.compile(r"<ELIF> (.+?) :IS NOT: \[(.+?)\](.*?)@\| OUTPUT \"(.+?)\" \|@")
        _21code = pattern.sub(self._translate_blackjack_elif, _21code)

        pattern = re.compile(r"<ELIF> (.+?) :IS BOTH: \[(.+?)\](.*?)@\| OUTPUT \"(.+?)\" \|@")
        _21code = pattern.sub(self._translate_blackjack_elif, _21code)

        # Repeat for other blackjack conditions (FLEXIBLE, NEITHER, etc.)
        return _21code

    def _translate_blackjack_if(self, match):
        var_name, condition, rest, output = match.groups()
        python_condition = self._convert_blackjack_condition(var_name, condition)
        return f'if {python_condition}:{rest}\n    print("{output}")'

    def _translate_blackjack_elif(self, match):
        var_name, condition, rest, output = match.groups()
        python_condition = self._convert_blackjack_condition(var_name, condition)
        return f'elif {python_condition}:{rest}\n    print("{output}")'

    def _convert_blackjack_condition(self, var_name, condition):
        """Converts a blackjack condition into Python condition syntax."""
        conditions = condition.split('and')
        python_conditions = []
        for cond in conditions:
            cond = cond.strip()
            if "greater than" in cond:
                python_conditions.append(f'{var_name} > {cond.split()[-1]}')
            elif "less than" in cond:
                python_conditions.append(f'{var_name} < {cond.split()[-1]}')
            elif "divisible by" in cond:
                python_conditions.append(f'{var_name} % {cond.split()[-1]} == 0')
        return ' and '.join(python_conditions)

    def translate_mutation_operations(self, _21code):
        """Translates mutation operations."""
        pattern = re.compile(r"~\| change (\w+) -> (\d+), (\w+) -> (\d+) \|~")
        return pattern.sub(lambda match: f'{match[1]} = {match[2]}\n{match[3]} = {match[4]}', _21code)

    def translate_user_prompts(self, _21code):
        """Translates user prompts and input requests."""
        pattern = re.compile(r"<ASK> \"(.+?)\"\s+-> store (\w+)@\| OUTPUT \"(.+?)\" \+ (\w+) \|@")
        return pattern.sub(self._translate_user_prompt, _21code)

    def _translate_user_prompt(self, match):
        prompt_message, input_var, output_text, output_var = match.groups()
        return f'{input_var} = input("{prompt_message}")\nprint("{output_text} " + {output_var})'


# Example 21-Style Pseudocode to Translate
_21code = """
~| var:int [ x = 10 ], var:bool [ flag = true ] |~
~| eax <- 5 |~
~| add eax, x |~
~| store eax -> result |~
<IF:blackjack> x :IS: [greater than 5 and less than 15] 
     @| OUTPUT "x is in range" |@
<ELIF> x :IS NOT: [5, 15] 
     @| OUTPUT "x is outside range" |@
<ELIF> x :IS BOTH: [greater than 5 and divisible by 2] 
     @| OUTPUT "x is both in range and even" |@
<ASK> "Please enter a value:" 
    -> store input_value
@| OUTPUT "You entered: " + input_value |@
"""

# Initialize and run translation
translator = _21Translator()
translated_code = translator.translate(_21code)
print(translated_code)
