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
