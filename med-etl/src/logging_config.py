# logging_config.py
"""Centralized logging configuration for med-etl application"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


def setup_logging():
    """
    Configure logging for the med-etl application.
    Creates both console and file handlers with appropriate formatting.
    """
    
    # Create log directory if it doesn't exist
    log_dir = Path(os.environ.get('LOG_DIRECTORY_PATH', './_log')) # get env value or use a default
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_filename = f"med-etl-{timestamp}.log"
    log_filepath = log_dir / log_filename
    
    # Create root logger for med-etl
    logger = logging.getLogger("med_etl")
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers to avoid duplication
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler for persistent logging
    file_handler = logging.FileHandler(log_filepath, mode='a', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Log the logging setup completion
    logger.info("Logging initialized - Log file: %s", log_filepath)
    
    return logger


def get_logger(name):
    """
    Get a logger instance for a specific module.
    
    Args:
        name (str): Usually __name__ from the calling module
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Ensure logging is set up
    root_logger = logging.getLogger("med_etl")
    if not root_logger.handlers:
        setup_logging()
    
    # Return child logger
    return logging.getLogger(f"med_etl.{name}")
