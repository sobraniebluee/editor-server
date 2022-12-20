import logging
from logging import Logger as LogerInterface
from src.config import Config


class Logger:
    def __init__(self, name):
        self.api_info: LogerInterface = self._create_logger('api_info', Config.LOGGER_API_INFO_FILEPATH, logging.INFO)
        self.db_error: LogerInterface = self._create_logger('db_error', Config.LOGGER_DB_FILEPATH, logging.ERROR)
        self.api_error: LogerInterface = self._create_logger('api_error', Config.LOGGER_API_ERROR_FILEPATH, logging.WARNING)

    @staticmethod
    def _create_logger(name, filepath, level):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
        file_handler = logging.FileHandler(filepath)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
