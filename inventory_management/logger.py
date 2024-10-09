import logging
from django.conf import settings
from datetime import datetime

class ErrorLogger(object):
    def __init__(self):
        # Create the Logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)

        # Convert BASE_DIR to string and create the path for the log file
        base_dir_str = str(settings.BASE_DIR)
        date = datetime.strftime(datetime.now(), '%d_%m_%Y')
        log_file_path = f"{base_dir_str}/log/{date}.log"

        # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler(log_file_path)
        logger_handler.setLevel(logging.ERROR)

        # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(asctime)s - %(pathname)s - %(lineno)d - %(module)s - %(funcName)s - %(levelname)s - %(message)s - %(user)s - %(details)s')

        # Add the Formatter to the Handler
        logger_handler.setFormatter(logger_formatter)

        # Add the Handler to the Logger
        self.logger.addHandler(logger_handler)

# Creating an instance of the ErrorLogger class
ins_logger = ErrorLogger()
