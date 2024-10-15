class ErrorHandler:
    @staticmethod
    def log_error(message):
        print(f"Error: {message}")

    @staticmethod
    def handle_exception(e):
        ErrorHandler.log_error(str(e))
        # More sophisticated error handling can be implemented here
