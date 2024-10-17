class BlackjackLogicHandler:
    def __init__(self):
        self.variables = {}

    def add_variable(self, var_name, value):
        self.variables[var_name] = value

    def check_state(self, var_name, conditions):
        value = self.variables.get(var_name)
        if not value:
            raise Exception(f"Variable '{var_name}' not found")

        results = []
        for condition in conditions:
            condition_type, cond_val = condition.split()
            cond_val = int(cond_val)

            if condition_type == "greater":
                if value > cond_val:
                    results.append(f"{var_name} is greater than {cond_val}")
            elif condition_type == "less":
                if value < cond_val:
                    results.append(f"{var_name} is less than {cond_val}")
            elif condition_type == "divisible":
                if value % cond_val == 0:
                    results.append(f"{var_name} is divisible by {cond_val}")
            else:
                results.append(f"Condition '{condition}' is not recognized.")

        return results

    def blackjack(self, var_name, conditions):
        results = self.check_state(var_name, conditions)
        if results:
            for result in results:
                print(result)
        else:
            print(f"No conditions met for {var_name}.")
