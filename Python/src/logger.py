import logging
from config import LOG_CRITICAL, LOG_CRITICAL_FORMAT


# logging parameters set up and create logger
def logger_setup():
    
    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    
    # create file handler which logs even debug messages
    log_handler_file = logging.FileHandler(LOG_CRITICAL, 'w')
    log_handler_file.setLevel(logging.CRITICAL)
    
    # create console handler
    log_handler_console = logging.StreamHandler()
    log_handler_console.setLevel(logging.CRITICAL)
    
    # create formatter and add it to the handlers
    formatter = logging.Formatter(LOG_CRITICAL_FORMAT)
    log_handler_file.setFormatter(formatter)
    log_handler_console.setFormatter(formatter)
    
    # add the handlers to the logger
    logger.addHandler(log_handler_file)
    logger.addHandler(log_handler_console)
    
    return logger         