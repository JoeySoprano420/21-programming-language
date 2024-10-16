class Context:
    def __init__(self):
        self.variables = {}
        self.state = None

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name):
        return self.variables.get(name)

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def reset(self):
        self.variables.clear()
        self.state = None
