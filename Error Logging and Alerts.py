import logging

class Logger:
    def __init__(self):
        logging.basicConfig(level=logging.ERROR, 
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def log_error(self, message):
        logging.error(message)

    def log_info(self, message):
        logging.info(message)

    def log_warning(self, message):
        logging.warning(message)


class AdvancedErrorHandler(ErrorHandler):
    def bait_and_switch(self, faulty_logic):
        try:
            # Attempt to execute logic
            self.execute_logic(faulty_logic)
        except Exception as e:
            self.handle_error(e)

    def type_check(self, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(f"Expected {expected_type}, got {type(value)}")
