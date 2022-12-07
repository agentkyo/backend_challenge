import logging
from datetime import datetime

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(name)s - %(levelname)s - %(message)s",
)


class Log:
    def __init__(self, name, level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.propagate = True

    def add_info(self, message, traceback_code):
        self.logger.info(f"{message} - {traceback_code}")
        print(f"INFO -> {datetime.now()} - {message} - {traceback_code}")

    def add_debug(self, message, traceback_code):
        self.logger.debug(f"{message} - {traceback_code}")
        print(f"DEBUG -> {datetime.now()} - {message} - {traceback_code}")

    def add_warning(self, message, traceback_code):
        self.logger.warning(f"{message} - {traceback_code}")
        print(f"WARNING -> {datetime.now()} - {message} - {traceback_code}")

    def add_error(self, message, traceback_code):
        self.logger.error(f"{message} - {traceback_code}")
        print(f"ERROR -> {datetime.now()} - {message} - {traceback_code}")

    def add_critical(self, message, traceback_code):
        self.logger.critical(f"{message} - {traceback_code}")
        print(f"CRITICAL -> {datetime.now()} - {message} - {traceback_code}")
