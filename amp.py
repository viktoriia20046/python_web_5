import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message: str):
    logging.info(message)

if __name__ == "__main__":
    setup_logging()
    log_message("AMP script initialized.")