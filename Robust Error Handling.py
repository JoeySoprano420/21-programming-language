class ErrorHandler:
    def handle_error(self, error):
        # Log the error details
        print(f"Error: {error}")
        
    def validate_condition(self, condition):
        if not isinstance(condition, (int, float, bool, str)):
            raise ValueError("Invalid condition type for evaluation.")

    def handle_logic_error(self, state_id):
        print(f"Invalid logic state ID: {state_id}. Please use a valid state ID (1-21).")
