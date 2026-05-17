import logging
import sys

class LogConfig:
    """
    Centralized logging configuration.
    """
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Returns a configured logger instance.
        """
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
